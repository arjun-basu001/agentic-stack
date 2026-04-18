from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cart import CartItem
from app.models.product import Product


class CartService:
    @staticmethod
    def add_item(db: Session, user_id: int, product_id: int, quantity: int) -> CartItem:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        item = db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.product_id == product_id).first()
        if item:
            item.quantity += quantity
        else:
            item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def list_items(db: Session, user_id: int) -> list[CartItem]:
        return db.query(CartItem).filter(CartItem.user_id == user_id).all()

    @staticmethod
    def clear_cart(db: Session, user_id: int) -> None:
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        db.commit()
