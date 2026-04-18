from collections import Counter

from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.models.product import Product


class RecommendationService:
    @staticmethod
    def recommend_for_user(db: Session, user_id: int, limit: int = 5) -> list[dict]:
        # Lightweight collaborative filtering baseline:
        # 1) infer category affinity from user's historical purchases
        # 2) combine with global popularity to produce ranked recommendations
        user_orders = db.query(Order.id).filter(Order.user_id == user_id).all()
        order_ids = [o.id for o in user_orders]

        category_scores: Counter[str] = Counter()
        if order_ids:
            for item in db.query(OrderItem).filter(OrderItem.order_id.in_(order_ids)).all():
                product = db.query(Product).filter(Product.id == item.product_id).first()
                if product:
                    category_scores[product.category] += item.quantity

        popularity: Counter[int] = Counter()
        for item in db.query(OrderItem).all():
            popularity[item.product_id] += item.quantity

        ranked = []
        for p in db.query(Product).all():
            score = 1.0
            score += category_scores.get(p.category, 0) * 0.5
            score += popularity.get(p.id, 0) * 0.1
            ranked.append({"id": p.id, "name": p.name, "category": p.category, "score": round(score, 2)})

        return sorted(ranked, key=lambda x: x["score"], reverse=True)[:limit]
