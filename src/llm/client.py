from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict

CACHE_DIR = Path("data/.cache/llm")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class ModelClient:
    """Minimal provider-agnostic LLM client stub with caching and cost logging.

    Real provider adapters should subclass/replace the internals here.
    """

    def __init__(self, pricing_table: Dict[str, float] | None = None):
        self.pricing_table = pricing_table or {}

    def _cache_key(self, payload: Dict[str, Any]) -> str:
        h = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        return h

    def generate(self, prompt: str, model_id: str = "default", temperature: float = 0.0) -> Dict[str, Any]:
        payload = {"prompt": prompt, "model_id": model_id, "temperature": temperature}
        key = self._cache_key(payload)
        cache_file = CACHE_DIR / f"{key}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())

        # Simulated call: deterministic stub output for now
        start = time.time()
        response = {
            "model": model_id,
            "prompt": prompt,
            "text": "[stub output]",
            "tokens_in": len(prompt.split()),
            "tokens_out": 1,
            "latency": 0.0,
        }
        latency = time.time() - start
        response["latency"] = latency

        # cost accounting
        ppm = self.pricing_table.get(model_id)
        if ppm is None:
            # fail loudly on unknown model cost assumptions
            raise RuntimeError(f"Unknown model id for pricing: {model_id}")
        response["cost"] = (response["tokens_in"] + response["tokens_out"]) * ppm

        cache_file.write_text(json.dumps(response))
        return response
