from fastapi import FastAPI
from api.v1.analysis import router as analysis_router

app = FastAPI(
    title="Market Analysis AI",
    version="1.0.0"
)

app.include_router(analysis_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}