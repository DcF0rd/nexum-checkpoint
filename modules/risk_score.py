"""Risk scoring engine for NEXUM-CHECKPOINT

Provides a simple rule-based scoring system and helpers to format deductions.
"""
from datetime import datetime
from typing import Dict, List, Tuple


DEFAULT_BASE = 100


class RiskScorer:
    def __init__(self, base: int = DEFAULT_BASE):
        self.base = base

    def calculate_score(self, findings: Dict) -> Tuple[int, List[Dict]]:
        """Calculate score and return (score, deductions_list).

        findings: a dict containing keys like 'firewall', 'antivirus', 'disk_encryption', 'user_accounts', 'updates'
        deductions_list: list of {"reason": str, "points": int}
        """
        score = self.base
        deductions = []

        # Firewall
        fw = findings.get("firewall") or {}
        fw_status = fw.get("status", "unknown").lower()
        if fw_status in ("off", "inactive", "disabled"):
            deductions.append({"reason": "Firewall is disabled", "points": 20})
            score -= 20

        # Antivirus
        av = findings.get("antivirus") or {}
        av_status = av.get("status", "unknown").lower()
        if av_status in ("off", "inactive", "disabled"):
            deductions.append({"reason": "Antivirus is not active", "points": 20})
            score -= 20

        # Disk encryption
        disk = findings.get("disk_encryption") or {}
        disk_status = disk.get("status", "unknown").lower()
        if disk_status in ("off", "unencrypted", "false"):
            deductions.append({"reason": "Disk is not encrypted", "points": 30})
            score -= 30

        # Guest account
        users = findings.get("user_accounts") or {}
        if users.get("guest_enabled"):
            deductions.append({"reason": "Guest account enabled", "points": 10})
            score -= 10

        # Updates
        updates = findings.get("updates")
        if updates is False:
            deductions.append({"reason": "Automatic updates disabled", "points": 10})
            score -= 10

        # Clamp
        if score < 0:
            score = 0
        if score > self.base:
            score = self.base

        return score, deductions


def interpret_band(score: int) -> Tuple[str, str]:
    """Return (band, color) for a numeric score."""
    if score >= 80:
        return "Secure", "green"
    if score >= 50:
        return "Needs Attention", "yellow"
    return "At Risk", "red"


def format_deductions(deductions: List[Dict]) -> str:
    lines = []
    for d in deductions:
        lines.append(f"- {d.get('reason')}: -{d.get('points')} pts")
    return "\n".join(lines)
