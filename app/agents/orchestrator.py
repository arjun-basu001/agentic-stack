from sqlalchemy.orm import Session

from app.agents.customer_service_agent import CustomerServiceAgent
from app.agents.inventory_agent import InventoryAgent
from app.agents.memory import PortableBrain
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.tools import ToolRegistry, ToolSpec
from app.services.inventory_service import InventoryService
from app.services.recommendation_service import RecommendationService


class AgentOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.brain = PortableBrain()
        self.tools = self._register_tools()
        self.recommendation_agent = RecommendationAgent("recommendation", self.brain, self.tools)
        self.customer_service_agent = CustomerServiceAgent("customer_service", self.brain, self.tools)
        self.inventory_agent = InventoryAgent("inventory", self.brain, self.tools)

    def _register_tools(self) -> ToolRegistry:
        tools = ToolRegistry()
        tools.register(
            ToolSpec(
                name="recommend_products",
                description="Get product recommendations for a user",
                run=lambda user_id: RecommendationService.recommend_for_user(self.db, user_id),
            )
        )
        tools.register(
            ToolSpec(
                name="get_inventory",
                description="Fetch inventory snapshot for a product",
                run=lambda product_id: {
                    "product_id": product_id,
                    "quantity_available": InventoryService.get_inventory(self.db, product_id).quantity_available,
                    "reorder_threshold": InventoryService.get_inventory(self.db, product_id).reorder_threshold,
                },
            )
        )
        return tools

    def run_recommendations(self, user_id: int) -> dict[str, object]:
        return self.recommendation_agent.handle({"user_id": user_id})

    def run_customer_service(self, message: str) -> dict[str, object]:
        return self.customer_service_agent.handle({"message": message})

    def run_inventory(self, product_id: int) -> dict[str, object]:
        return self.inventory_agent.handle({"product_id": product_id})
