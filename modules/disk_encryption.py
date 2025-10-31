import platform
import subprocess
import os

def get_encryption_status():
    """Check disk encryption status based on the operating system."""
    system = platform.system().lower()
    
    if system == "windows":
        try:
            # Check BitLocker status using manage-bde
            cmd = ["manage-bde", "-status"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if "Protection On" in result.stdout:
                return {"status": "encrypted", "type": "BitLocker"}
            elif "Protection Off" in result.stdout:
                return {"status": "not encrypted", "type": "BitLocker available"}
            else:
                return {"status": "unknown", "type": "BitLocker not available"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    elif system == "linux":
        try:
            # Check LUKS encryption
            cmd = ["lsblk", "-f"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if "crypto_LUKS" in result.stdout:
                return {"status": "encrypted", "type": "LUKS"}
            else:
                return {"status": "not encrypted", "type": "No LUKS detected"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    elif system == "darwin":  # macOS
        try:
            # Check FileVault status
            cmd = ["fdesetup", "status"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if "FileVault is On" in result.stdout:
                return {"status": "encrypted", "type": "FileVault"}
            elif "FileVault is Off" in result.stdout:
                return {"status": "not encrypted", "type": "FileVault available"}
            else:
                return {"status": "unknown", "type": "FileVault status unknown"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    return {"status": "unknown", "error": "Unsupported operating system"}