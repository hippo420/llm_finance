from typing import List
from langchain_core.documents import Document

def es_reports_retriever(query: str) -> List[Document]:
    """
    ElasticSearch - 증권사 리포트 Retriever
    """

    # TODO:
    # - ES reports index 검색
    # - 최신순 + 신뢰도 가중치
    # - summary / opinion / target_price 추출

    mock_report = (
        "증권사: NH투자증권\n"
        "투자의견: BUY\n"
        "요약: 메모리 반도체 수요 회복으로 실적 개선 전망\n"
        "목표가: 92,000원"
    )

    return [
        Document(
            page_content=f"[증권사 리포트]\n{mock_report}",
            metadata={
                "source": "NH투자증권",
                "type": "report"
            }
        )
    ]