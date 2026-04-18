from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class ToolSpec:
    name: str
    description: str
    run: Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, tool: ToolSpec) -> None:
        self._tools[tool.name] = tool

    def call(self, tool_name: str, **kwargs: Any) -> Any:
        if tool_name not in self._tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        return self._tools[tool_name].run(**kwargs)

    def list_tools(self) -> list[dict[str, str]]:
        return [{"name": t.name, "description": t.description} for t in self._tools.values()]
