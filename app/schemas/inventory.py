from pydantic import BaseModel


class InventoryUpdate(BaseModel):
    quantity_available: int
    reorder_threshold: int | None = None


class InventoryOut(BaseModel):
    product_id: int
    quantity_available: int
    reorder_threshold: int
