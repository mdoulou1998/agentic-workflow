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
client = ModelClient(model_name="gpt-4", api_key="your_api_key_here")
out =  retrieval.retrieve(doc, client, config={})
print(json.dumps(out, indent=2, default=str))