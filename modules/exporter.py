"""Export utilities for NEXUM-CHECKPOINT

Exports data to JSON and Markdown. Keeps exports in an `exports/` directory
by default.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


BASE_DIR = Path(__file__).parent.parent
EXPORTS_DIR = BASE_DIR / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)


def export_json(data: Dict[str, Any], filename: str = None) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = filename or f"audit_{ts}.json"
    path = EXPORTS_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    return path


def export_markdown(data: Dict[str, Any], filename: str = None) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = filename or f"audit_{ts}.md"
    path = EXPORTS_DIR / filename

    # Basic markdown representation
    with open(path, "w", encoding="utf-8") as f:
        f.write("# NEXUM-CHECKPOINT Audit\n\n")
        f.write(f"Export Date: {datetime.now().isoformat()}\n\n")
        # If data contains timestamp and os info, include
        osinfo = data.get("os")
        if osinfo:
            f.write("## System Information\n")
            f.write(f"- OS: {osinfo.get('name', '')} {osinfo.get('version', '')}\n\n")

        # Score if present
        if "risk_score" in data:
            f.write(f"## Risk Score: {data.get('risk_score')}\n\n")

        f.write("## Findings\n")
        f.write("```")
        f.write(json.dumps(data.get("findings", data), indent=2, default=str))
        f.write("\n```\n")

    return path
