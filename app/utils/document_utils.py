from typing import Dict, List
from langchain_core.documents import Document

def combine_documents(docs_dict: Dict[str, List[Document]]) -> str:
    """
    여러 Retriever 결과를 하나의 context 문자열로 결합
    """

    sections = []

    if docs_dict.get("postgres"):
        sections.append(
            "--- 시세 / 수급 데이터 ---\n"
            + "\n".join(d.page_content for d in docs_dict["postgres"])
        )

    if docs_dict.get("reports"):
        sections.append(
            "--- 증권사 리포트 ---\n"
            + "\n".join(d.page_content for d in docs_dict["reports"])
        )

    if docs_dict.get("news"):
        sections.append(
            "--- 뉴스 ---\n"
            + "\n".join(d.page_content for d in docs_dict["news"])
        )

    return "\n\n".join(sections)