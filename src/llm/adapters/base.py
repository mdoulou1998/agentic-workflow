from __future__ import annotations

from typing import Any, Dict, Protocol


class Adapter(Protocol):
    """Normalized interface every provider adapter must implement.

    `call` returns a dict with exactly: text, tokens_in, tokens_out.
    Cost, caching, and latency stay in ModelClient — adapters know nothing
    about pricing or the disk cache.
    """

    def call(self, prompt: str, model: str, temperature: float) -> Dict[str, Any]: ...