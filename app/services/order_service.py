from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.services.cart_service import CartService
from app.services.inventory_service import InventoryService


class OrderService:
    @staticmethod
    def checkout(db: Session, user_id: int) -> Order:
        cart_items = CartService.list_items(db, user_id)
        if not cart_items:
            raise ValueError("Cart is empty")

        order = Order(user_id=user_id, status="PLACED", total_amount=0)
        db.add(order)
        db.flush()

        total = 0.0
        for item in cart_items:
            InventoryService.reserve_stock(db, item.product_id, item.quantity)
            line_total = item.product.price * item.quantity
            total += line_total
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    product_name=item.product.name,
                    quantity=item.quantity,
                    unit_price=item.product.price,
                )
            )

        order.total_amount = total
        CartService.clear_cart(db, user_id)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def list_orders(db: Session, user_id: int) -> list[Order]:
        return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()
