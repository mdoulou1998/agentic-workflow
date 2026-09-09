# STATE

M0 - Skeleton: completed. Contracts, adapters, and agent stubs added.

Progress highlights:
- Provider spike executed and recorded in `data/provider_spike.json` (live Gemini + mock results).
- Adapter implementations: `MockAdapter` and `GeminiAdapter` with Chat API preference added.
- `ModelClient` implemented: provider-agnostic, caching, and cost accounting.
- Config: `config/models.json` introduced; model selection centralized via `src/config/models.py`.
- Scripts: `scripts/provider_spike.py` and `run_retrieval.py` updated to use config-driven model selection and to safely read `GEMINI_API_KEY`.
- Tests: initial unit tests added (`tests/test_contracts.py`, `tests/test_client.py`, `tests/test_retrieval.py`, `tests/test_provider_config.py`) — test suite passes locally.
- Documentation: `docs/DECISIONS.md` updated with provider-spike ADR and rationale.

Next milestones:
- Add broader unit test coverage for pipeline orchestration and adapters with mocking.
- Add CI workflow to run tests/linting on push.
- Instrument per-stage tracing, cost logging, and evaluation harness (M1–M3 work).
