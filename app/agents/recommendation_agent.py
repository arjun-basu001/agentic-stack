from app.agents.base import BaseAgent


class RecommendationAgent(BaseAgent):
    def handle(self, payload: dict[str, int]) -> dict[str, object]:
        user_id = payload["user_id"]
        recommendations = self.tools.call("recommend_products", user_id=user_id)
        self.observe("recommendations_generated", {"user_id": user_id, "count": len(recommendations)})
        return {"user_id": user_id, "recommendations": recommendations}
