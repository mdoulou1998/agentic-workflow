import json
from pathlib import Path


def test_models_config_exists_and_has_providers():
    p = Path("config/models.json")
    assert p.exists(), "config/models.json must exist"
    cfg = json.loads(p.read_text())
    assert "providers" in cfg and isinstance(cfg["providers"], dict)
