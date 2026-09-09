from __future__ import annotations

from typing import Any, Dict, List

from ..contracts import Critique


def critique_mappings(mappings: List[Dict[str, Any]], client: Any, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Stub critique agent. Returns a list of critique dicts (Pydantic `model_dump` shape).

    Empty stub returns an empty list to keep the API stable for downstream code.
    """
    return []
