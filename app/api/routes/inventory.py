from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.inventory import InventoryOut, InventoryUpdate
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/{product_id}", response_model=InventoryOut)
def get_inventory(product_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> InventoryOut:
    inv = InventoryService.get_inventory(db, product_id)
    return InventoryOut(
        product_id=inv.product_id,
        quantity_available=inv.quantity_available,
        reorder_threshold=inv.reorder_threshold,
    )


@router.put("/{product_id}", response_model=InventoryOut)
def update_inventory(
    product_id: int,
    payload: InventoryUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> InventoryOut:
    inv = InventoryService.update_stock(db, product_id, payload.quantity_available, payload.reorder_threshold)
    return InventoryOut(
        product_id=inv.product_id,
        quantity_available=inv.quantity_available,
        reorder_threshold=inv.reorder_threshold,
    )
