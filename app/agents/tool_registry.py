from typing import Dict


class ToolRegistry:
    """Registry for tools used in the graph."""

    def __init__(self):
        self._tools: Dict[str, object] = {}

    def register(self, name: str, tool: object):
        self._tools[name] = tool

    def get(self, name: str):
        return self._tools.get(name)

    def all(self) -> Dict[str, object]:
        return self._tools