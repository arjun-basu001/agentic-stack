from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float
    category: str


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str

    class Config:
        from_attributes = True
