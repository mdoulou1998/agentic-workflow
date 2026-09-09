import json
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_CONFIG_PATH = Path("config/models.json")


def load_models_config(path: Optional[str] = None) -> Dict[str, Any]:
    p = Path(path) if path else DEFAULT_CONFIG_PATH
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def get_default_model(provider: str, path: Optional[str] = None, fallback: Optional[str] = None) -> Optional[str]:
    cfg = load_models_config(path)
    providers = cfg.get("providers", {}) if isinstance(cfg, dict) else {}
    val = providers.get(provider)
    if isinstance(val, list) and len(val) > 0:
        return val[0]
    return fallback
