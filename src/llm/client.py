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

    This class is intentionally small: it normalises model calls, performs
    deterministic caching by payload hash, and computes cost from a
    `pricing_table` keyed by `model_id`.

    To support different providers or free models (e.g. Gemini mini or other
    public/free models), you can pass provider kwargs like `model_name` or
    `api_key` here. Set `allow_unknown_pricing=True` to permit unknown model
    IDs (cost will be recorded as 0.0).
    """

    def __init__(
        self,
        pricing_table: Dict[str, float] | None = None,
        default_model: str | None = None,
        allow_unknown_pricing: bool = False,
        **provider_kwargs: Any,
    ):
        self.pricing_table = pricing_table or {}
        self.default_model = default_model
        self.allow_unknown_pricing = allow_unknown_pricing
        # store provider-specific configuration (api_key, model_name, etc.)
        self.provider_kwargs = provider_kwargs

    def _cache_key(self, payload: Dict[str, Any]) -> str:
        # include provider kwargs so different API keys/models don't collide
        full = {**payload, "provider": self.provider_kwargs}
        h = hashlib.sha256(json.dumps(full, sort_keys=True).encode()).hexdigest()
        return h

    def generate(self, prompt: str, model_id: str | None = None, temperature: float = 0.0) -> Dict[str, Any]:
        """Generate text from the given prompt.

        If `model_id` is omitted the client's `default_model` or `provider_kwargs['model_name']`
        will be used if present.
        """

        model = model_id or self.default_model or self.provider_kwargs.get("model_name", "default")
        payload = {"prompt": prompt, "model_id": model, "temperature": temperature}
        key = self._cache_key(payload)
        cache_file = CACHE_DIR / f"{key}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())

        # Simulated call: deterministic stub output for now
        start = time.time()
        response = {
            "model": model,
            "prompt": prompt,
            "text": "[stub output]",
            "tokens_in": len(prompt.split()),
            "tokens_out": 1,
            "latency": 0.0,
        }
        latency = time.time() - start
        response["latency"] = latency

        # cost accounting
        ppm = self.pricing_table.get(model)
        if ppm is None:
            if self.allow_unknown_pricing:
                response["cost"] = 0.0
            else:
                # fail loudly on unknown model cost assumptions to avoid silent zero-cost runs
                raise RuntimeError(f"Unknown model id for pricing: {model}")
        else:
            response["cost"] = (response["tokens_in"] + response["tokens_out"]) * ppm

        cache_file.write_text(json.dumps(response))
        return response
