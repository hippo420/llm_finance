from typing import List
from langchain_core.documents import Document

def postgres_retriever(query: str) -> List[Document]:
    """
    Postgres에서 정형 시세/수급 Feature를 조회하는 Retriever
    (실제 구현 시 SQLAlchemy or langchain_postgres 사용)
    """

    # TODO:
    # 1. query에서 종목코드 추출
    # 2. 최근 N일 시세/수급 집계
    # 3. Feature dict 생성

    mock_feature = (
        "최근 20거래일 기준\n"
        "- 종가 추세: 상승\n"
        "- 거래량 추세: 증가\n"
        "- 외국인 수급: 순매수 전환\n"
        "- 기관 수급: 중립\n"
        "- 변동성: 중간"
    )

    return [
        Document(
            page_content=f"[Postgres Feature]\n{mock_feature}"
        )
    ]