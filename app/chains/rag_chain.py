from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from retrievers import (
    postgres_retriever,
    es_reports_retriever,
    es_news_retriever,
)
from prompts.qa_prompt import QA_PROMPT
from utils.document_utils import combine_documents
from llm.qwen import get_qwen_llm


def build_rag_chain():
    llm = get_qwen_llm()

    parallel_retrievers = RunnableParallel(
        postgres=postgres_retriever,
        reports=es_reports_retriever,
        news=es_news_retriever,
    )

    chain = (
        {
            "context": parallel_retrievers | combine_documents,
            "question": RunnablePassthrough(),
        }
        | QA_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain