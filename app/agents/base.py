import logging
from abc import ABC, abstractmethod
from typing import Any

from app.agents.memory import PortableBrain
from app.agents.tools import ToolRegistry


class BaseAgent(ABC):
    def __init__(self, name: str, brain: PortableBrain, tools: ToolRegistry) -> None:
        self.name = name
        self.brain = brain
        self.tools = tools
        self.logger = logging.getLogger(f"agent.{name}")

    def observe(self, event_type: str, payload: dict[str, Any]) -> None:
        self.logger.info("agent_event", extra={"agent": self.name, "event_type": event_type, "payload": payload})
        self.brain.log_episode(self.name, event_type, payload)

    @abstractmethod
    def handle(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
