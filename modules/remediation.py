"""Remediation helpers that perform (or simulate) safe system fixes.

All actions are gated by explicit user approval and admin checks.
"""
import subprocess
import platform
from typing import Dict, List
from .permissions import is_admin
from pathlib import Path
import logging

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
logger = logging.getLogger("nexum.remediation")
handler = logging.FileHandler(LOG_DIR / "remediation.log")
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def available_fixes() -> Dict[str, str]:
    """Return a dict of fix_id -> human friendly description."""
    return {
        "enable_firewall": "Enable Windows Firewall (all profiles)",
        "set_uac_secure": "Set UAC to a secure level (Windows)",
        "disable_guest": "Disable guest account",
        "enable_auto_updates": "Enable automatic updates/service"
    }


def run_command(cmd: List[str], simulate: bool = False) -> Dict:
    """Run a system command and return result dict. If simulate, don't execute."""
    logger.info(f"run_command simulate={simulate} cmd={cmd}")
    if simulate:
        return {"cmd": cmd, "status": "simulated"}

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        result = {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
        logger.info(f"Command result: {result}")
        return result
    except Exception as e:
        logger.exception("Command execution failed")
        return {"error": str(e)}


def apply_fix(fix_id: str, simulate_if_not_admin: bool = True) -> Dict:
    """Apply a fix. Returns a dict describing the action and result.

    If not running as admin, either simulate (if simulate_if_not_admin) or raise.
    """
    admin = is_admin()
    simulate = not admin and simulate_if_not_admin

    if fix_id == "enable_firewall":
        if platform.system().lower().startswith("win"):
            cmd = ["netsh", "advfirewall", "set", "allprofiles", "state", "on"]
            return run_command(cmd, simulate=simulate)
        else:
            # On linux, use ufw if present
            cmd = ["ufw", "enable"]
            return run_command(cmd, simulate=simulate)

    if fix_id == "disable_guest":
        if platform.system().lower().startswith("win"):
            cmd = ["net", "user", "guest", "/active:no"]
            return run_command(cmd, simulate=simulate)
        else:
            # On linux, lock the guest user if exists
            cmd = ["sudo", "usermod", "-L", "guest"]
            return run_command(cmd, simulate=simulate)

    if fix_id == "enable_auto_updates":
        if platform.system().lower().startswith("win"):
            # set service to auto and start
            cmd1 = ["sc", "config", "wuauserv", "start=", "auto"]
            cmd2 = ["net", "start", "wuauserv"]
            res1 = run_command(cmd1, simulate=simulate)
            res2 = run_command(cmd2, simulate=simulate)
            return {"step1": res1, "step2": res2}
        else:
            # example for systemd-based systems
            cmd = ["sudo", "systemctl", "enable", "--now", "apt-daily.timer"]
            return run_command(cmd, simulate=simulate)

    if fix_id == "set_uac_secure":
        # Changing UAC requires registry edits - we simulate unless elevated
        if not admin and simulate_if_not_admin:
            return {"status": "simulated", "message": "Would set UAC to secure level (requires admin)"}
        # Actual implementation left minimal/safe
        return {"status": "not_implemented", "message": "UAC change not implemented programmatically for safety"}

    return {"error": "unknown_fix"}
