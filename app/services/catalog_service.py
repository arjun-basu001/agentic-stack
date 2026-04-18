from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


class CatalogService:
    @staticmethod
    def list_products(db: Session, category: str | None = None) -> list[Product]:
        query = db.query(Product)
        if category:
            query = query.filter(Product.category == category)
        return query.order_by(Product.id.desc()).all()

    @staticmethod
    def create_product(db: Session, payload: ProductCreate) -> Product:
        product = Product(**payload.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
