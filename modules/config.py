"""Simple configuration storage for toggles like Offline Mode."""
from pathlib import Path
import json

CONFIG_FILE = Path(__file__).parent.parent / "config.json"


DEFAULTS = {"offline_mode": False}


def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**DEFAULTS, **data}
        except Exception:
            return DEFAULTS.copy()
    return DEFAULTS.copy()


def save_config(cfg: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
