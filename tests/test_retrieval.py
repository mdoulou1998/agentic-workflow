from src.contracts.models import EvidenceDocument
from src.agents.retrieval import retrieve
from src.llm.client import ModelClient


def test_retrieval_returns_structure():
    doc = EvidenceDocument(id="d1", title="t", text="I wrote a data pipeline and tests", source=None)
    client = ModelClient(provider="mock", default_model="mock", allow_unknown_pricing=True)
    out = retrieve(doc, client, config={})
    assert isinstance(out, dict)
    assert "retrieved_ksbs" in out
