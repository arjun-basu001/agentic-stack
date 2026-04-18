from app.agents.base import BaseAgent


class InventoryAgent(BaseAgent):
    def handle(self, payload: dict[str, int]) -> dict[str, object]:
        product_id = payload["product_id"]
        inventory = self.tools.call("get_inventory", product_id=product_id)

        action = "none"
        if inventory["quantity_available"] <= inventory["reorder_threshold"]:
            action = "reorder_required"

        self.observe("inventory_checked", {"product_id": product_id, "action": action})
        return {"inventory": inventory, "action": action}
