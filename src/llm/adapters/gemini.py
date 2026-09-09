from __future__ import annotations

import os
from typing import Any, Dict

try:
    from google import genai
except ImportError:
    genai = None  # surfaced at construction time, not import time


class GeminiAdapter:
    """Thin adapter for Google's Gemini API.

    Targets the `google-genai` package (`uv add google-genai`), which is
    Google's current SDK as of my last check — they have shipped more than
    one Python SDK for Gemini (the older `google-generativeai` uses a
    different client shape), so verify this is still current before relying
    on it; I haven't confirmed it against today's docs.

    Reads the API key from `GEMINI_API_KEY` unless passed explicitly.
    """

    def __init__(self, api_key: str | None = None):
        if genai is None:
            raise ImportError("google-genai not installed. Run: uv add google-genai")
        self.client = genai.Client(api_key=api_key or os.environ.get("GEMINI_API_KEY"))

    def call(self, prompt: str, model: str, temperature: float) -> Dict[str, Any]:
        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
            config={"temperature": temperature},
        )
        usage = getattr(response, "usage_metadata", None)
        tokens_in = getattr(usage, "prompt_token_count", 0) if usage else 0
        tokens_out = getattr(usage, "candidates_token_count", 0) if usage else 0
        return {"text": response.text, "tokens_in": tokens_in, "tokens_out": tokens_out}