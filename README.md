# Market Analysis AI (LLM Finance)
# LLM Finance (Text-to-SQL RAG)

**Market Analysis AI**는 RAG(Retrieval-Augmented Generation) 기술을 기반으로 금융 데이터를 분석하여 투자 인사이트를 제공하는 AI 서비스입니다.
금융 데이터 질의를 위한 Text-to-SQL RAG 시스템입니다.
사용자의 자연어 질문을 SQL로 변환하여 DB에서 데이터를 조회합니다.

정형 데이터(시세, 수급)와 비정형 데이터(증권사 리포트, 뉴스)를 결합하여 LLM(Qwen)이 논리적이고 보수적인 시장 분석 리포트를 작성합니다.
## 주요 기능

## 🚀 주요 기능
1. **Schema Vectorization**: 서버 시작 시 DB 스키마(DDL)를 벡터화하여 ChromaDB에 저장.
2. **Schema Linking**: 사용자 질문과 관련된 테이블을 벡터 검색으로 식별.
3. **Text-to-SQL**: 검색된 스키마 정보를 바탕으로 LLM이 SQL 생성.

- **멀티 소스 RAG (Multi-Source RAG)**
  - **Postgres**: 시세, 수급 등 정형 데이터 조회
  - **ElasticSearch**: 증권사 리포트 및 뉴스 검색
  - `LangChain`의 `RunnableParallel`을 사용하여 3가지 소스를 병렬로 검색
## 사전 요구사항 (Prerequisites)

- **고성능 캐싱 시스템 (Redis)**
  - 분석 결과에 대해 Redis 캐싱 적용 (TTL 5분)
  - **Cache Stampede 방지**: 동일한 쿼리에 대해 동시에 여러 요청이 올 경우, 분산 락(Lock)을 사용하여 LLM 중복 호출 방지
*   **Python**: 3.10+
*   **PostgreSQL**: 금융 데이터 저장소
*   **Ollama**: 로컬 LLM 실행 (모델: `qwen:7b`, `nomic-embed-text`)
*   **ChromaDB**: 벡터 데이터베이스 (Schema 저장용)

- **LLM 통합**
  - `Ollama`를 통해 로컬에서 구동되는 **Qwen:7b** 모델 사용
  - 금융 분석에 특화된 프롬프트 엔지니어링 (근거 기반, 보수적 서술)
## 설치 및 실행

- **데이터 결합 및 Fallback 처리**
  - 뉴스나 리포트가 없을 경우, 시세 데이터만으로 분석하도록 자동 분기 처리 (`document_utils.py`)
### 1. 환경 설정

## 📂 프로젝트 구조

```bash
llm_finance/
├── app/
│   ├── api/            # API 엔드포인트 (v1)
│   ├── chains/         # LangChain RAG 파이프라인 구성
│   ├── infra/          # Redis 등 인프라 설정
│   ├── config.py       # 설정 파일 로더
│   ├── db.py           # PostgreSQL 연결 관리
│   ├── es.py           # ElasticSearch 연결 관리
│   ├── llm.py          # LLM 모델 설정 (Qwen/Ollama)
│   ├── prompts/        # 프롬프트 템플릿 관리
│   ├── retrievers/     # 데이터 검색 모듈 (Postgres, ES)
│   ├── schemas/        # Pydantic 데이터 모델
│   ├── utils/          # 유틸리티 (캐시 키 생성, 문서 병합)
│   └── main.py         # FastAPI 진입점
├── config.ini          # 프로젝트 설정 파일 (DB, ES, LLM)
└── README.md
pip install -r requirements.txt
```

## 🛠️ 기술 스택
### 2. 설정 파일 (config.ini)

- **Language**: Python 3.10+
- **Web Framework**: FastAPI
- **LLM Orchestration**: LangChain
- **LLM Serving**: Ollama (Model: qwen:7b)
- **Database / Search**:
  - Redis (Caching & Locking)
  - PostgreSQL (Simulated)
  - ElasticSearch (Simulated)
`config.ini` 파일을 프로젝트 루트에 생성하고 DB 및 LLM 설정을 입력합니다.

## ⚙️ 설치 및 실행 방법
```ini
[PostgreSQL]
host = localhost
port = 5432
database = finadm
...

### 1. 사전 요구사항 (Prerequisites)
[LLM]
model_name = qwen:7b
base_url = http://localhost:11434

- **Redis**: 로컬 또는 원격 Redis 서버가 실행 중이어야 합니다.
- **Ollama**: 로컬에 Ollama가 설치되어 있어야 하며, Qwen 모델이 필요합니다.
  ```bash
  ollama pull qwen:7b
  ```
[Chroma]
host = localhost
port = 8000
collection_name = schema_store
```

### 2. 환경 변수 설정
### 3. ChromaDB 실행 (Server Mode)

필요에 따라 환경 변수를 설정합니다. (기본값 내장됨)
- `REDIS_HOST`: Redis 호스트 (기본값: localhost)
- `REDIS_PORT`: Redis 포트 (기본값: 6379)

### 3. 서버 실행

```bash
# 의존성 설치 (예시)
pip install fastapi uvicorn langchain langchain-community redis

# 앱 실행
uvicorn app.main:app --reload
chroma run --path ./chroma_data --port 8000
```

## 📡 API 사용법
### 4. 서버 실행

### 시장 분석 요청

- **Endpoint**: `POST /api/v1/analysis`
- **Content-Type**: `application/json`

**Request Body:**
```json
{
  "query": "삼성전자 최근 주가 흐름과 전망 분석해줘"
}
```bash
uvicorn main:app --reload
```

**Response:**
```json
{
  "answer": "핵심 요약: ... \n\n근거: ... \n\n주의사항: ..."
}
```