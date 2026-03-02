import chromadb
from typing import List, Dict
from sqlalchemy import text
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document

from app.config import Config
from db import create_db_engine

class SchemaLoader:
    def __init__(self):
        self.config = Config()
        self.chroma_config = self.config.get_chroma_config()
        self.llm_config = self.config.get_llm_config()
        
        # Initialize Embedding Model (using Ollama to match llm.py)
        self.embedding_function = OllamaEmbeddings(
            base_url=self.llm_config.get("base_url", "http://localhost:11434"),
            model="nomic-embed-text" # Recommended for embeddings, or use config value
        )

    def load(self):
        """
        Server startup task:
        1. Fetch Table DDLs
        2. Vectorize and store in Chroma
        """
        print("Starting Schema Vectorization...")
        
        # 1. Get DDLs
        schemas = self._fetch_ddls()
        
        if not schemas:
            print("No schemas found to vectorize.")
            return

        # 2. Store in Chroma
        self._store_vectors(schemas)
        print(f"Successfully vectorized {len(schemas)} tables.")

    def _fetch_ddls(self) -> List[Dict[str, str]]:
        """
        Connects to DB and retrieves DDL for all relevant tables.
        Returns a list of dicts: {'table_name': str, 'ddl': str}
        """
        engine = create_db_engine()
        results = []

        with engine.connect() as conn:
            sql = text("""
                SELECT 
                    table_name,
                    'CREATE TABLE ' || table_name || ' (' || chr(10) ||
                    string_agg(
                        '    ' || rpad(column_name, 20) || ' ' || rpad(data_type, 15) || 
                        CASE WHEN is_nullable = 'NO' THEN ' NOT NULL' ELSE '         ' END ||
                        ' -- ' || COALESCE(
                            (SELECT d.description 
                             FROM pg_description d 
                             JOIN pg_class c ON d.objoid = c.oid 
                             JOIN pg_attribute a ON c.oid = a.attrelid AND d.objsubid = a.attnum
                             WHERE c.relname = cols.table_name 
                               AND a.attname = cols.column_name), 
                            '설명 없음'
                        ),
                        ',' || chr(10) ORDER BY ordinal_position
                    ) || chr(10) || ');' AS final_ddl
                FROM information_schema.columns cols
                WHERE table_name IN ('stock_trade', 'info_stock')
                  AND table_schema = 'public'
                GROUP BY table_name;
            """)
            rows = conn.execute(sql).fetchall()
            for row in rows:
                results.append({"table_name": row.table_name, "ddl": row.final_ddl})

        return results

    def _store_vectors(self, schemas: List[Dict[str, str]]):
        """
        Embeds DDLs and saves them to Chroma (localhost:8000)
        """
        host = self.chroma_config.get("host", "localhost")
        port = int(self.chroma_config.get("port", "8000"))
        collection_name = self.chroma_config.get("collection_name", "schema_store")

        # Connect to Chroma Server
        client = chromadb.HttpClient(host=host, port=port)
        
        # Convert to LangChain Documents
        print("Table Names:", [item['table_name'] for item in schemas])
        documents = [
            Document(
                page_content=item['ddl'],
                metadata={"table_name": item['table_name']}
            ) for item in schemas
        ]

        # Create/Update VectorStore
        # This will automatically embed the 'page_content' (DDL)
        try:
            Chroma.from_documents(
                documents=documents,
                embedding=self.embedding_function,
                client=client,
                collection_name=collection_name
            )
            print(f"Vector DB Save Success: {len(documents)} documents saved to {collection_name}")
        except Exception as e:
            print(f"Vector DB Save Failed: {e}")
            raise e