# 분석 API 엔드포인트 - 레디스 중복질의 캐싱처리
import json
import time
from fastapi import APIRouter, HTTPException

from schemas.analysis import AnalysisRequest, AnalysisResponse
from chains.rag_chain import build_rag_chain
from infra.redis_client import redis_client
from utils.cache_utils import make_cache_key

router = APIRouter(prefix="/api/v1/analysis", tags=["Analysis"])

rag_chain = build_rag_chain()

CACHE_TTL = 300          # 5분
LOCK_TTL = 30            # 30초
WAIT_INTERVAL = 0.3      # 대기 polling


@router.post("", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    query = request.query.strip()
    cache_key = make_cache_key(query)
    lock_key = f"lock:{cache_key}"

    # 캐시 HIT
    cached = redis_client.get(cache_key)
    if cached:
        return AnalysisResponse(answer=cached)

    # Lock 시도 (SETNX)
    acquired = redis_client.set(lock_key, "1", nx=True, ex=LOCK_TTL)

    if acquired:
        #내가 LLM 호출 담당
        try:
            result = rag_chain.invoke(query)

            redis_client.set(
                cache_key,
                result,
                ex=CACHE_TTL
            )
            return AnalysisResponse(answer=result)

        finally:
            redis_client.delete(lock_key)

    else:
        #다른 요청이 처리 중 → 결과 대기
        wait_time = 0.0

        while wait_time < LOCK_TTL:
            time.sleep(WAIT_INTERVAL)
            wait_time += WAIT_INTERVAL

            cached = redis_client.get(cache_key)
            if cached:
                return AnalysisResponse(answer=cached)

        raise HTTPException(
            status_code=504,
            detail="Analysis in progress. Please retry."
        )