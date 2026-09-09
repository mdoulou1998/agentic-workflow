from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict

from .adapters.base import Adapter
from .adapters.mock import MockAdapter
from .adapters.gemini import GeminiAdapter

CACHE_DIR = Path("data/.cache/llm")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

_ADAPTERS: Dict[str, type] = {
    "mock": MockAdapter,
    "gemini": GeminiAdapter,
}


class ModelClient:
    """Provider-agnostic LLM client: caching and cost accounting live here;
    everything provider-specific lives in `adapters/`.

    `provider` selects the adapter ("mock" or "gemini"). `provider_kwargs`
    (e.g. `api_key`) are passed straight to that adapter's constructor.
    """

    def __init__(
        self,
        pricing_table: Dict[str, float] | None = None,
        default_model: str | None = None,
        provider: str = "mock",
        allow_unknown_pricing: bool = False,
        **provider_kwargs: Any,
    ):
        if provider not in _ADAPTERS:
            raise ValueError(f"Unknown provider '{provider}'. Known: {list(_ADAPTERS)}")
        self.pricing_table = pricing_table or {}
        self.default_model = default_model
        self.allow_unknown_pricing = allow_unknown_pricing
        self.provider = provider
        self._adapter: Adapter = _ADAPTERS[provider](**provider_kwargs)

    def _cache_key(self, payload: Dict[str, Any]) -> str:
        full = {**payload, "provider": self.provider}
        h = hashlib.sha256(json.dumps(full, sort_keys=True).encode()).hexdigest()
        return h

    def generate(self, prompt: str, model_id: str | None = None, temperature: float = 0.0) -> Dict[str, Any]:
        model = model_id or self.default_model
        if model is None:
            raise ValueError("No model_id given and no default_model configured.")

        payload = {"prompt": prompt, "model_id": model, "temperature": temperature}
        key = self._cache_key(payload)
        cache_file = CACHE_DIR / f"{key}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())

        start = time.time()
        result = self._adapter.call(prompt, model, temperature)
        latency = time.time() - start

        response = {
            "model": model,
            "prompt": prompt,
            "text": result["text"],
            "tokens_in": result["tokens_in"],
            "tokens_out": result["tokens_out"],
            "latency": latency,
        }

        ppm = self.pricing_table.get(model)
        if ppm is None:
            if self.allow_unknown_pricing:
                response["cost"] = 0.0
            else:
                raise RuntimeError(f"Unknown model id for pricing: {model}")
        else:
            response["cost"] = (response["tokens_in"] + response["tokens_out"]) * ppm

        cache_file.write_text(json.dumps(response))
        return response