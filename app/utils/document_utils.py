from typing import Dict, List
from langchain_core.documents import Document


def combine_documents(docs_dict: Dict[str, List[Document]]) -> str:
    """
    Retriever 결과를 조합하되
    뉴스/리포트가 없을 경우 자동 fallback 처리
    """

    postgres_docs = docs_dict.get("postgres", [])
    report_docs = docs_dict.get("reports", [])
    news_docs = docs_dict.get("news", [])

    sections = []

    # 시세/수급 (항상 포함)
    if postgres_docs:
        sections.append(
            "--- 시세 / 수급 데이터 ---\n"
            + "\n".join(d.page_content for d in postgres_docs)
        )

    #리포트 / 뉴스 상태 판단
    has_reports = len(report_docs) > 0
    has_news = len(news_docs) > 0

    #정상 케이스
    if has_reports:
        sections.append(
            "--- 증권사 리포트 ---\n"
            + "\n".join(d.page_content for d in report_docs)
        )

    if has_news:
        sections.append(
            "--- 뉴스 ---\n"
            + "\n".join(d.page_content for d in news_docs)
        )

    #Fallback 안내 문구 (LLM 안정화용)
    if not has_reports and not has_news:
        sections.append(
            "--- 참고 사항 ---\n"
            "현재 시점에 수집된 뉴스 및 증권사 리포트가 없습니다.\n"
            "아래 분석은 시세 및 수급 데이터만을 기반으로 합니다."
        )

    elif not has_reports:
        sections.append(
            "--- 참고 사항 ---\n"
            "증권사 리포트 데이터가 없어 뉴스 및 시세 데이터 중심으로 분석합니다."
        )

    elif not has_news:
        sections.append(
            "--- 참고 사항 ---\n"
            "최근 뉴스 데이터가 없어 리포트 및 시세 데이터 중심으로 분석합니다."
        )

    return "\n\n".join(sections)