from pydantic import BaseModel


class SearchResult(BaseModel):
    id: int
    name: str
    category: str
    score: float


class RecommendationResponse(BaseModel):
    user_id: int
    recommendations: list[SearchResult]
