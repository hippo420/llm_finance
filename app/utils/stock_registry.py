from typing import Dict
from infra.db import SessionLocal
from sqlalchemy import text


class StockRegistry:
    def __init__(self):
        self.alias_map: Dict[str, str] = {}

    def load(self):
        print("Loading stock registry...")
        """
        앱 기동 시 1회 호출
        stock_alias 테이블을 전부 메모리에 적재
        """
        sql = text("""
            SELECT isu_srt_cd AS 종목코드, isu_abbrv AS 종목명
            FROM info_stock
        """)

        session = SessionLocal()
        try:
            rows = session.execute(sql).fetchall()

            self.alias_map = {
                row.alias: row.stock_code
                for row in rows
            }

        finally:
            session.close()

    def resolve(self, token: str) -> str | None:
        if not token:
            return None
        return self.alias_map.get(token.lower())