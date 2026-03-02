import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from sqlalchemy import text
from langchain_core.prompts import ChatPromptTemplate

from app.utils.schema_loader import SchemaLoader
from app.utils.schema_retriever import SchemaRetriever
from app.prompts.sql_prompt import SQL_PROMPT
from llm import load_llm
from db import create_db_engine

# 최종 답변 생성을 위한 프롬프트
ANSWER_PROMPT = ChatPromptTemplate.from_template(
    """
    You are a helpful AI assistant. Based on the user's question and the data retrieved from the database, provide a clear and concise answer in Korean.
    Do not mention that the data was retrieved from a database. Just answer the question based on the data.

    User's Question: {question}

    Retrieved Data:
    {data}
    """
)

# 전역 인스턴스
retriever = None
llm = None
db_engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global retriever, llm, db_engine
    
    # 0. 중복 적재 방지를 위해 기존 벡터 DB 초기화
    print(">>> Clearing existing Schema Vector Store...")
    try:
        # SchemaRetriever를 임시로 사용하여 DB 접속 및 컬렉션 삭제
        temp_retriever = SchemaRetriever()
        collection_name = temp_retriever.db._collection.name
        temp_retriever.client.delete_collection(collection_name)
        print(f">>> Collection '{collection_name}' cleared.")
    except Exception as e:
        print(f">>> Collection clear skipped (might be empty): {e}")

    # 1. 서버 시작 시 스키마 벡터화 (Loader 실행)
    print(">>> Initializing Schema Loader...")
    loader = SchemaLoader()
    loader.load()
    
    # 2. 검색기, LLM, DB 엔진 초기화
    retriever = SchemaRetriever()
    llm = load_llm()
    db_engine = create_db_engine()
    
    yield
    
    # 종료 시 리소스 정리
    pass

app = FastAPI(lifespan=lifespan)

class ChatRequest(BaseModel):
    question: str
    instructions: str = "특이사항 없음"  # SQL 생성 시 반영할 추가 지침 (기본값 설정)

@app.post("/chat")
def chat(req: ChatRequest):
    # 1. 관련 스키마 검색 (RAG)
    relevant_schemas = retriever.get_relevant_schemas(req.question)
    print(f"Relevant Schemas:\n{len(relevant_schemas)} schemas found")
    
    if not relevant_schemas:
        return {"message": "관련된 테이블 정보를 찾을 수 없습니다."}

    # make_sql_instructions.dat 파일에서 지침 읽기
    instruction_file = "make_sql_instructions.dat"
    file_instructions = ""
    if os.path.exists(instruction_file):
        with open(instruction_file, "r", encoding="utf-8") as f:
            file_instructions = f.read().strip()

    # 파일 지침과 사용자 요청 지침 결합 (기본값 '특이사항 없음' 제외)
    user_instructions = req.instructions if req.instructions != "특이사항 없음" else ""
    final_instructions = f"{file_instructions}\n{user_instructions}".strip() or "특이사항 없음"

    # 2. LLM을 통한 SQL 생성
    chain = SQL_PROMPT | llm
    response = chain.invoke({
        "context": relevant_schemas,
        "question": req.question,
        "instructions": final_instructions
    })
    
    # LLM이 생성한 SQL에서 마크다운 코드 블록 제거
    sql_query = response.content.strip().replace("```sql", "").replace("```", "")
    print(f"Generated SQL: {sql_query}")

    # 3. SQL 실행 및 결과 반환
    try:
        with db_engine.connect() as conn:
            result = conn.execute(text(sql_query))
            db_data = [dict(row._mapping) for row in result]
    except Exception as e:
        return {
            "question": req.question,
            "generated_sql": sql_query,
            "answer": f"SQL 실행 중 오류가 발생했습니다: {str(e)}"
        }

    if not db_data:
        return {
            "question": req.question,
            "generated_sql": sql_query,
            "answer": "데이터베이스에서 관련 정보를 찾을 수 없었습니다."
        }

    # 4. 조회된 데이터를 바탕으로 최종 답변 생성
    answer_chain = ANSWER_PROMPT | llm
    final_response = answer_chain.invoke({"question": req.question, "data": db_data})

    return {
        "question": req.question,
        "generated_sql": sql_query,
        "answer": final_response.content
    }

if __name__ == "__main__":
    import uvicorn
    from config import Config

    config = Config()
    server_config = config.get_server_config()
    host = server_config.get("host", "0.0.0.0")
    port = int(server_config.get("port", 31111))

    # reload=True를 적용하려면 app 객체 대신 "모듈명:앱객체" 문자열을 사용해야 합니다.
    uvicorn.run("main:app", host=host, port=port, reload=True)