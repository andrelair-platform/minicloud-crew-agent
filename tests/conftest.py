"""Mock heavy AI/HTTP deps so tests run without a running cluster."""
import sys
from unittest.mock import MagicMock

_crewai = MagicMock(name="crewai")
for mod in ("crewai", "crewai.tools"):
    sys.modules.setdefault(mod, _crewai)

_pydantic = sys.modules.get("pydantic")  # keep real pydantic if present

_ddgs = MagicMock(name="ddgs")
sys.modules.setdefault("ddgs", _ddgs)

_httpx = MagicMock(name="httpx")
sys.modules.setdefault("httpx", _httpx)
