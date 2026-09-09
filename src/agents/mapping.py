from __future__ import annotations

from typing import Any, Dict, List

from ..contracts import Mapping, Claim


def map_claims(claims: List[Claim], client: Any, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Stub mapping agent: map claims to KSB codes.

    Returns a list of mapping dicts (Pydantic `model_dump()` shape).
    Empty stub returns an empty list to keep the API stable.
    """
    # Example future implementation would return Mapping(...).model_dump()
    return []
