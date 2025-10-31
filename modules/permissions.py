"""Permission and elevation helpers

Simple cross-platform detection of admin/root privileges.
"""
import os
import sys

def is_admin() -> bool:
    try:
        if sys.platform.startswith("win"):
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except Exception:
        return False


def require_admin_or_raise():
    if not is_admin():
        raise PermissionError("This action requires administrator privileges.")
