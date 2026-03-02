import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from app.config import Config

class SchemaRetriever:
    def __init__(self):
        self.config = Config()
        chroma_conf = self.config.get_chroma_config()
        llm_conf = self.config.get_llm_config()

        # Embedding 설정 (Loader와 동일하게 유지)
        self.embedding_function = OllamaEmbeddings(
            base_url=llm_conf.get("base_url", "http://localhost:11434"),
            model="nomic-embed-text"
        )

        # Chroma Server 연결
        self.client = chromadb.HttpClient(
            host=chroma_conf.get("host", "localhost"),
            port=int(chroma_conf.get("port", "8000"))
        )
        
        self.db = Chroma(
            client=self.client,
            collection_name=chroma_conf.get("collection_name", "schema_store"),
            embedding_function=self.embedding_function
        )

    def get_relevant_schemas(self, query: str, k: int = 3) -> str:
        """질문과 유사한 테이블 스키마(DDL) 검색"""
        docs = self.db.similarity_search(query, k=k)
        #print(f"Retrieved {docs} relevant schemas for query: '{query}'")
        # 검색된 DDL들을 하나의 문자열로 결합하여 프롬프트 컨텍스트용으로 반환
        return "\n\n".join([doc.page_content for doc in docs])