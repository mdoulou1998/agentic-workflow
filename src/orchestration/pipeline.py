from __future__ import annotations

from typing import Any, Dict

from ..contracts import EvidenceDocument
from ..llm.client import ModelClient
from ..agents import retrieval, extraction, mapping, critique


def run_pipeline(document: EvidenceDocument, client: ModelClient, config: Dict[str, Any]) -> Dict[str, Any]:
    trace = {"document_id": document.id, "stages": {}}

    candidates = retrieval.retrieve(document, client, config.get("retrieval", {}))
    trace["stages"]["retrieval"] = {"count": len(candidates)}

    claims = extraction.extract(document, client, config.get("extraction", {}))
    trace["stages"]["extraction"] = {"count": len(claims)}

    mappings = mapping.map_claims(claims, client, config.get("mapping", {}))
    trace["stages"]["mapping"] = {"count": len(mappings)}

    critiques = critique.critique_mappings(mappings, client, config.get("critique", {}))
    trace["stages"]["critique"] = {"count": len(critiques)}

    return trace
