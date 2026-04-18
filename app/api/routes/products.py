from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.product import ProductCreate, ProductOut
from app.services.catalog_service import CatalogService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductOut])
def list_products(category: str | None = None, db: Session = Depends(get_db)) -> list[ProductOut]:
    return CatalogService.list_products(db, category)


@router.post("/", response_model=ProductOut)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ProductOut:
    return CatalogService.create_product(db, payload)
