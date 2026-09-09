from __future__ import annotations

from typing import Any, Dict


class MockAdapter:
    """Deterministic, no-network stub. Default for tests and offline dev."""

    def call(self, prompt: str, model: str, temperature: float) -> Dict[str, Any]:
        return {
            "text": "[stub output]",
            "tokens_in": len(prompt.split()),
            "tokens_out": 1,
        }