"""Run a small provider spike: send the same prompt to two providers and
write side-by-side results for decision evidence.

Outputs: `data/provider_spike.json` with a dict keyed by provider name.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

HERE = Path(__file__).parent.parent
import sys
# ensure repo root is on sys.path so `src` imports work when running this script
sys.path.insert(0, str(HERE))
from src.llm.client import ModelClient
OUT = HERE / "data" / "provider_spike.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

try:
    from dotenv import load_dotenv

    load_dotenv()
    import dotenv as _dotenv
    print("dotenv loaded from:", getattr(_dotenv, "__file__", "<unknown>"))
except Exception:
    pass

PROMPT = (
    'Extract discrete competence claims from the following evidence: "I wrote a data pipeline and ran some tests" and return a short summary.'
)

def call_provider(provider: str, model: str | None = None, provider_kwargs: dict | None = None):
    provider_kwargs = provider_kwargs or {}
    results = {"provider": provider, "model": model, "ok": False}
    try:
        client = ModelClient(
            provider=provider,
            default_model=model,
            pricing_table={model: 0.0} if model else {},
            allow_unknown_pricing=True,
            **provider_kwargs,
        )
        start = time.time()
        resp = client.generate(PROMPT, model_id=model)
        elapsed = time.time() - start
        results.update({
            "ok": True,
            "text": resp.get("text"),
            "tokens_in": resp.get("tokens_in"),
            "tokens_out": resp.get("tokens_out"),
            "cost": resp.get("cost"),
            "latency": resp.get("latency", elapsed),
        })
    except Exception as e:
        results.update({"error": str(e)})
    return results


def main():
    gemini_key = os.environ.get("GEMINI_API_KEY")

    providers = [
        ("mock", "mock", {}),
        ("gemini", "gemini-3.6-flash", {"api_key": gemini_key} if gemini_key else {}),
    ]

    out = {p: call_provider(p, m, kw) for p, m, kw in providers}

    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print("Wrote provider spike output to", OUT)


if __name__ == "__main__":
    main()
