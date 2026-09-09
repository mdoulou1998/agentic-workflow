from src.contracts.models import EvidenceDocument
from src.llm.client import ModelClient
from src.agents import retrieval
import json

doc = EvidenceDocument(
    id="doc1",
    title="Sample Document",
    text="I wrote a data pipeline and ran some tests",
    source=None
)
# Use `default_model` and allow unknown pricing when testing free or new models
client = ModelClient(default_model="gpt-4", allow_unknown_pricing=True, api_key="your_api_key_here")
out =  retrieval.retrieve(doc, client, config={})
print(json.dumps(out, indent=2, default=str))