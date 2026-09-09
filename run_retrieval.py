from src.contracts.models import EvidenceDocument
from src.llm.client import ModelClient
from src.agents import retrieval
import json
import os

try:
    # optional: load .env if python-dotenv is installed and a .env file exists
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

doc = EvidenceDocument(
    id="doc1",
    title="Sample Document",
    text="I wrote a data pipeline and ran some tests",
    source=None,
)

# Read the API key from the environment. Do not print the key directly.
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY not set in environment; add it to .env or export it in your shell")

# Use the mock provider for a dry-run to verify the key is passed through
client = ModelClient(provider="mock", default_model="mock", allow_unknown_pricing=True, api_key=api_key)

# Safe confirmation: show that the key was received by the client (length only)
masked = f"<redacted length={len(api_key)}>"
print("GEMINI_API_KEY loaded and passed to ModelClient as provider kwarg:", masked)

out = retrieval.retrieve(doc, client, config={})
print(json.dumps(out, indent=2, default=str))
