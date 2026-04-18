from pydantic import BaseModel


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: str
    unit_price: float


class CartSummary(BaseModel):
    items: list[CartItemOut]
    total_amount: float
