# Decisions (ADRs)

1. Initial skeleton uses hand-rolled orchestration and provider-agnostic LLM client stub.

2. Provider spike (2026-09-09): ran an experiment sending one prompt to two adapters (`mock` and `gemini`) and recorded responses and costs in [data/provider_spike.json](data/provider_spike.json).

- Outcome: `mock` returned the expected stub output; `gemini` returned an API error indicating the requested model id is unavailable on the current SDK (see the JSON for full error). The raw spike file is the evidence for this decision.

Decision: keep the adapter boundary and provider-agnostic `ModelClient`, but pin provider model IDs in `pyproject.toml`/docs and prefer a small integration-test that runs only when credentials and the target SDK are present. We will not hard-wire Gemini model ids in code; instead record them in a `config/models.yml` or similar and update when we reconfirm availability.
