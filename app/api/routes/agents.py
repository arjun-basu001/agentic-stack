from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.agents.orchestrator import AgentOrchestrator
from app.models.user import User

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("/recommend")
def agent_recommend(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, object]:
    orchestrator = AgentOrchestrator(db)
    return orchestrator.run_recommendations(user.id)


@router.post("/support")
def agent_support(message: str, _: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, object]:
    orchestrator = AgentOrchestrator(db)
    return orchestrator.run_customer_service(message)


@router.get("/inventory/{product_id}")
def agent_inventory(product_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, object]:
    orchestrator = AgentOrchestrator(db)
    return orchestrator.run_inventory(product_id)
