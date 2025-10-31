import platform
import subprocess
import json

def get_av_status():
    """Check antivirus status based on the operating system."""
    system = platform.system().lower()
    
    if system == "windows":
        try:
            # Using PowerShell to get Windows Defender status
            cmd = ["powershell", "-Command", 
                  "Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled, AntivirusEnabled | ConvertTo-Json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                status = json.loads(result.stdout)
                return {
                    "name": "Windows Defender",
                    "status": "active" if status.get("RealTimeProtectionEnabled") else "inactive",
                    "realtime_protection": status.get("RealTimeProtectionEnabled", False)
                }
        except Exception as e:
            return {"status": "unknown", "error": str(e)}
            
    elif system == "linux":
        # Check for common Linux antiviruses
        av_list = ["clamav", "sophos-av", "comodo"]
        for av in av_list:
            try:
                result = subprocess.run(["which", av], capture_output=True, text=True)
                if result.returncode == 0:
                    return {"name": av, "status": "installed"}
            except Exception:
                continue
        return {"status": "not detected"}
            
    elif system == "darwin":  # macOS
        try:
            # Check XProtect status
            result = subprocess.run(
                ["defaults", "read", "/Library/Preferences/com.apple.security", "XProtectEnabled"],
                capture_output=True,
                text=True
            )
            return {
                "name": "XProtect",
                "status": "active" if result.stdout.strip() == "1" else "inactive"
            }
        except Exception as e:
            return {"status": "unknown", "error": str(e)}
    
    return {"status": "unknown", "error": "Unsupported operating system"}