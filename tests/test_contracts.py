from src.contracts.models import EvidenceDocument


def test_evidence_document_roundtrip():
    doc = EvidenceDocument(id="doc1", title="t", text="some text", source=None)
    assert doc.id == "doc1"
