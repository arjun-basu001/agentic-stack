from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.inventory import Inventory


class InventoryService:
    @staticmethod
    def get_inventory(db: Session, product_id: int) -> Inventory:
        inv = db.query(Inventory).filter(Inventory.product_id == product_id).first()
        if not inv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
        return inv

    @staticmethod
    def reserve_stock(db: Session, product_id: int, quantity: int) -> None:
        inv = InventoryService.get_inventory(db, product_id)
        if inv.quantity_available < quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")
        inv.quantity_available -= quantity

    @staticmethod
    def update_stock(db: Session, product_id: int, quantity_available: int, reorder_threshold: int | None) -> Inventory:
        inv = InventoryService.get_inventory(db, product_id)
        inv.quantity_available = quantity_available
        if reorder_threshold is not None:
            inv.reorder_threshold = reorder_threshold
        db.commit()
        db.refresh(inv)
        return inv
