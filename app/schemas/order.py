from datetime import datetime

from pydantic import BaseModel


class OrderItemOut(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: float


class OrderOut(BaseModel):
    id: int
    status: str
    total_amount: float
    created_at: datetime
    items: list[OrderItemOut]
