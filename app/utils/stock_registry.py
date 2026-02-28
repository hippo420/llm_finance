from typing import Dict
from infra.db import SessionLocal
from sqlalchemy import text


class StockRegistry:
    def __init__(self):
        self.alias_map: Dict[str, str] = {}

    def load(self):
        """
        앱 기동 시 1회 호출
        stock_alias 테이블을 전부 메모리에 적재
        """
        sql = text("""
            SELECT LOWER(alias) AS alias, stock_code
            FROM stock_alias
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