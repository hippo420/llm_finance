from typing import List
from langchain_core.documents import Document

def es_news_retriever(query: str) -> List[Document]:
    """
    ElasticSearch - 뉴스 Retriever
    """

    # TODO:
    # - ES news index 검색
    # - 최근 1~3일
    # - sentiment_score 기준 필터

    mock_news = (
        "요약: AI 서버 수요 증가로 반도체 업황 개선 기대\n"
        "키워드: AI, 반도체, 서버\n"
        "감정 점수: 7.8 (긍정)"
    )

    return [
        Document(
            page_content=f"[뉴스]\n{mock_news}",
            metadata={
                "type": "news",
                "sentiment": 7.8
            }
        )
    ]