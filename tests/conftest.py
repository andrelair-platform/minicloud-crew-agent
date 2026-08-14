"""Mock heavy AI/HTTP deps so tests run without a running cluster."""

import sys
from unittest.mock import MagicMock

from pydantic import BaseModel

# BaseTool must be a real pydantic class, not a MagicMock.
# Subclassing a MagicMock creates a metaclass conflict when starlette
# imports pydantic BaseModel subclasses during TestClient setup.
class _BaseTool(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    name: str = ""
    description: str = ""

    def _run(self, *args, **kwargs):
        return ""


_crewai_tools = MagicMock(name="crewai.tools")
_crewai_tools.BaseTool = _BaseTool

_crewai = MagicMock(name="crewai")
sys.modules.setdefault("crewai", _crewai)
sys.modules.setdefault("crewai.tools", _crewai_tools)

_ddgs = MagicMock(name="ddgs")
sys.modules.setdefault("ddgs", _ddgs)
