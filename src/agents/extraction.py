from __future__ import annotations

from typing import Any, Dict, List

from ..contracts import Claim, EvidenceDocument


def extract(document: EvidenceDocument, client: Any, config: Dict[str, Any]) -> List[Claim]:
    """Stub extraction agent. Returns list of `Claim` instances.

    Should produce verbatim spans and locators.
    """
    # trivial: no claims
    return []
