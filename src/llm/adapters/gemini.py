from __future__ import annotations

import os
from typing import Any, Dict
from dotenv import load_dotenv

try:
    from google import genai
except ImportError:
    genai = None  # surfaced at construction time, not import time

try:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
except Exception:
    pass  # ignore if .env not present



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
        # Prefer the Chat API if available to avoid AFC warnings and follow
        # SDK guidance. Fall back to models.generate_content for older SDKs.
        # Both branches try to extract `text` and token usage metadata.
        # Chat API path (recommended):
        chat = getattr(self.client, "chat", None)
        if chat is not None:
            try:
                # recommended Chat API use
                resp = chat.send_message(model=model, input=prompt)
                # response shapes can vary; try common attributes
                text = getattr(resp, "text", None) or getattr(resp, "output", None)
                if text is None:
                    # some SDKs expose content differently
                    text = getattr(resp, "content", None) or str(resp)
                usage = getattr(resp, "usage_metadata", None) or getattr(resp, "usage", None)
                tokens_in = getattr(usage, "prompt_token_count", 0) if usage else 0
                tokens_out = getattr(usage, "candidates_token_count", 0) if usage else 0
                return {"text": text, "tokens_in": tokens_in, "tokens_out": tokens_out}
            except Exception:
                # if Chat API call fails, fall back to models.generate_content below
                pass

        # Fallback: models.generate_content (older SDKs)
        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
            config={"temperature": temperature},
        )
        usage = getattr(response, "usage_metadata", None) or getattr(response, "usage", None)
        tokens_in = getattr(usage, "prompt_token_count", 0) if usage else 0
        tokens_out = getattr(usage, "candidates_token_count", 0) if usage else 0
        text = getattr(response, "text", None) or getattr(response, "output", None) or str(response)
        return {"text": text, "tokens_in": tokens_in, "tokens_out": tokens_out}