from src.contracts.models import EvidenceDocument
from src.llm.client import ModelClient
from src.agents.retrieval import retrieve


def test_smoke_end_to_end_mock():
    doc = EvidenceDocument(id="smoke1", title="smoke", text="smoke test text", source=None)
    client = ModelClient(provider="mock", default_model="mock", allow_unknown_pricing=True)
    out = retrieve(doc, client, config={})
    assert isinstance(out, dict)
    assert "retrieved_ksbs" in out
