from __future__ import annotations

from typing import Any, Dict

from ..contracts import EvidenceDocument
from ..contracts.retrieval import RetrievalOutput, KSB


def retrieve(document: EvidenceDocument, client: Any, config: Dict[str, Any]) -> Dict[str, Any]:
    """Simple demo retrieval implementation.

    This mocked implementation looks for obvious keywords in the document text
    and returns a small set of KSB matches with provenance and confidence.
    It's intended only for local demos and tests until a real retrieval
    implementation (MCP/tool-backed) is provided.
    """
    text = (document.text or "").lower()
    ksbs = []
    rank = 1
    if "pipeline" in text or "data pipeline" in text:
        ksbs.append(
            KSB(
                ksb_code="S1",
                category="skills",
                description="Built and maintained data pipelines",
                source_locator="standards/engineering.md#S1",
                confidence=0.9,
                rank=rank,
            )
        )
        rank += 1
    if "test" in text or "tests" in text:
        ksbs.append(
            KSB(
                ksb_code="K2",
                category="knowledge",
                description="Understands testing and validation",
                source_locator="standards/engineering.md#K2",
                confidence=0.85,
                rank=rank,
            )
        )

    output = RetrievalOutput(
        standard_id="ENG-001",
        standard_title="Engineering Apprenticeship Standard (demo)",
        retrieved_ksbs=ksbs,
        retrieval_strategy=config.get("strategy", "keyword"),
        model_id=getattr(client, "default_model", None),
        prompt_version="retrieval_v1",
    )

    return output.model_dump()
