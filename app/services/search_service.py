from sqlalchemy.orm import Session

from app.models.product import Product


class SearchService:
    @staticmethod
    def search_products(db: Session, query: str) -> list[dict]:
        q = query.lower().strip()
        products = db.query(Product).all()
        results: list[dict] = []
        for p in products:
            text = f"{p.name} {p.description} {p.category}".lower()
            score = 0.0
            if q in p.name.lower():
                score += 2.0
            if q in p.category.lower():
                score += 1.5
            if q in text:
                score += 1.0
            if score > 0:
                results.append({"id": p.id, "name": p.name, "category": p.category, "score": score})

        return sorted(results, key=lambda r: r["score"], reverse=True)
