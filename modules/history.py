"""History storage helpers for past scans."""
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List

HISTORY_DIR = Path(__file__).parent.parent / "history"
HISTORY_DIR.mkdir(exist_ok=True)


def save_scan(data: Dict) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = HISTORY_DIR / f"scan_{ts}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    return path


def list_scans() -> List[Path]:
    files = sorted(HISTORY_DIR.glob("scan_*.json"), reverse=True)
    return files


def load_scan(path: Path) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
