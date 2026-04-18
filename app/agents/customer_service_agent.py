from app.agents.base import BaseAgent


class CustomerServiceAgent(BaseAgent):
    def handle(self, payload: dict[str, object]) -> dict[str, object]:
        user_message = str(payload.get("message", "")).lower()
        preferences = self.brain.read_preferences()
        tone = preferences.get("support_tone", "professional")

        if "refund" in user_message:
            response = "I can help initiate a refund workflow. Please share your order id."
        elif "status" in user_message:
            response = "I can check your latest order status. Please provide order id or continue to /orders endpoint."
        else:
            response = "I can assist with orders, returns, account, and recommendations."

        self.observe("customer_support_response", {"tone": tone, "message": user_message[:120]})
        return {"response": response, "tone": tone}
