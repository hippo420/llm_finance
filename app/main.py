from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.v1.analysis import router as analysis_router
from utils.stock_registry import StockRegistry

#전역 Registry 인스턴스
stock_registry = StockRegistry()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 앱 기동 / 종료 시점 훅
    """
    #기동 시 1회 로드
    stock_registry.load()
    print(f"[Startup] StockRegistry loaded ({len(stock_registry.alias_map)} aliases)")

    yield

    #종료 시 (필요 시 정리)
    print("[Shutdown] Application shutdown")


app = FastAPI(
    title="Market Analysis AI",
    version="1.0.0",
    lifespan=lifespan
)

# 라우터 등록
app.include_router(analysis_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}