from __future__ import annotations

from typing import Dict, Any, List

from ..contracts import EvidenceDocument


def retrieve(document: EvidenceDocument, client: Any, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Stub retrieval agent. Returns a list of candidate standards (minimal shape).

    The real implementation talks to the MCP corpus via a tool client.
    """
    # naive dummy: return an empty list
    return []
