from __future__ import annotations

from typing import Any, Dict


class MockAdapter:
    """Deterministic, no-network stub. Default for tests and offline dev."""

    def __init__(self, **kwargs: Any):
        # accept and ignore any provider kwargs (api_key, model_name, etc.)
        return None

    def call(self, prompt: str, model: str, temperature: float) -> Dict[str, Any]:
        return {
            "text": "[stub output]",
            "tokens_in": len(prompt.split()),
            "tokens_out": 1,
        }