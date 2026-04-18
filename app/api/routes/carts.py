from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemOut, CartSummary
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=CartSummary)
def list_cart(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> CartSummary:
    items = CartService.list_items(db, user.id)
    output = [
        CartItemOut(
            id=i.id,
            product_id=i.product_id,
            quantity=i.quantity,
            product_name=i.product.name,
            unit_price=i.product.price,
        )
        for i in items
    ]
    total = sum(i.unit_price * i.quantity for i in output)
    return CartSummary(items=output, total_amount=total)


@router.post("/items", response_model=CartItemOut)
def add_to_cart(payload: CartItemCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> CartItemOut:
    item = CartService.add_item(db, user.id, payload.product_id, payload.quantity)
    return CartItemOut(
        id=item.id,
        product_id=item.product_id,
        quantity=item.quantity,
        product_name=item.product.name,
        unit_price=item.product.price,
    )
