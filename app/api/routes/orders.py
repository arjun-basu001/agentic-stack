from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.order import OrderItemOut, OrderOut
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/checkout", response_model=OrderOut)
def checkout(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> OrderOut:
    try:
        order = OrderService.checkout(db, user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return OrderOut(
        id=order.id,
        status=order.status,
        total_amount=order.total_amount,
        created_at=order.created_at,
        items=[
            OrderItemOut(
                product_id=i.product_id,
                product_name=i.product_name,
                quantity=i.quantity,
                unit_price=i.unit_price,
            )
            for i in order.items
        ],
    )


@router.get("/", response_model=list[OrderOut])
def list_orders(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[OrderOut]:
    orders = OrderService.list_orders(db, user.id)
    return [
        OrderOut(
            id=o.id,
            status=o.status,
            total_amount=o.total_amount,
            created_at=o.created_at,
            items=[
                OrderItemOut(
                    product_id=i.product_id,
                    product_name=i.product_name,
                    quantity=i.quantity,
                    unit_price=i.unit_price,
                )
                for i in o.items
            ],
        )
        for o in orders
    ]
