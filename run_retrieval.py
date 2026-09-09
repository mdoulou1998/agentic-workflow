from src.contracts.models import EvidenceDocument
from src.llm.client import ModelClient
from src.agents import retrieval
import json
import os

try:
    # optional: load .env if python-dotenv is installed and a .env file exists
    from dotenv import load_dotenv
    load_dotenv()
    # help diagnose which package provided `dotenv`
    import dotenv as _dotenv
    try:
        print("dotenv module loaded from:", getattr(_dotenv, "__file__", "<builtin>"))
    except Exception:
        pass
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

# Try to use the Gemini adapter if available; fall back to mock for dry-run
try:
    client = ModelClient(
        provider="gemini",
        default_model="gemini-2.0-flash",
        pricing_table={"gemini-2.0-flash": 0.0},
        api_key=api_key,
    )
    using = "gemini"
except Exception as e:
    # adapter unavailable (e.g., google-genai not installed) or other error
    print("Gemini adapter unavailable, falling back to mock adapter:", str(e))
    client = ModelClient(provider="mock", default_model="mock", allow_unknown_pricing=True, api_key=api_key)
    using = "mock"

# Safe confirmation: show that the key was received by the client (length only)
masked = f"<redacted length={len(api_key)}>"
print(f"GEMINI_API_KEY loaded; using provider={using}; key={masked}")

out = retrieval.retrieve(doc, client, config={})
print(json.dumps(out, indent=2, default=str))
