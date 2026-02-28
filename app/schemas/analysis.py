from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    query: str


class AnalysisResponse(BaseModel):
    answer: str