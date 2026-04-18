from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.search import RecommendationResponse, SearchResult
from app.services.recommendation_service import RecommendationService
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/products", response_model=list[SearchResult])
def search_products(q: str, db: Session = Depends(get_db)) -> list[SearchResult]:
    return [SearchResult(**r) for r in SearchService.search_products(db, q)]


@router.get("/recommendations", response_model=RecommendationResponse)
def recommendations(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> RecommendationResponse:
    recs = RecommendationService.recommend_for_user(db, user.id)
    return RecommendationResponse(user_id=user.id, recommendations=[SearchResult(**r) for r in recs])
