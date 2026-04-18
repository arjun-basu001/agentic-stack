from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.user import User


def seed_data(db: Session) -> None:
    if db.query(User).count() > 0:
        return

    user = User(email="admin@agentic-commerce.local", hashed_password=hash_password("admin123"), is_active=True)
    db.add(user)

    catalog = [
        Product(name="Enterprise Laptop", description="High-performance laptop", price=1499.0, category="electronics"),
        Product(name="Wireless Keyboard", description="Mechanical keyboard", price=129.0, category="electronics"),
        Product(name="Noise-Canceling Headphones", description="Premium ANC headset", price=299.0, category="electronics"),
        Product(name="Standing Desk", description="Adjustable ergonomic desk", price=499.0, category="furniture"),
    ]
    db.add_all(catalog)
    db.flush()

    for p in catalog:
        db.add(Inventory(product_id=p.id, quantity_available=100, reorder_threshold=10))

    db.commit()
