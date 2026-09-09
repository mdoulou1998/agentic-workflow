from src.contracts.models import EvidenceDocument
from src.llm.client import ModelClient
from src.agents import retrieval
import json

doc = EvidenceDocument(
    id="doc1",
    title="Sample Document",
    text="I wrote a data pipeline and ran some tests",
    source=None,
)

# Free-tier Gemini. Requires GEMINI_API_KEY in the environment.
# Pricing entered explicitly at 0.0 rather than allow_unknown_pricing=True,
# so a real paid model slipping in later still fails loudly.
client = ModelClient(
    provider="gemini",
    default_model="gemini-2.0-flash",
    pricing_table={"gemini-2.0-flash": 0.0},
)
out = retrieval.retrieve(doc, client, config={})
print(json.dumps(out, indent=2, default=str))