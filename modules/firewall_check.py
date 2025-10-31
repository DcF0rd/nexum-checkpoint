import platform
import subprocess

def get_status():
    """Check firewall status based on the operating system."""
    system = platform.system().lower()
    
    if system == "windows":
        try:
            # Check Windows Defender Firewall status
            result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles"], 
                capture_output=True, 
                text=True
            )
            return {"status": "active" if "ON" in result.stdout else "inactive"}
        except Exception as e:
            return {"status": "unknown", "error": str(e)}
            
    elif system == "linux":
        try:
            # Check UFW status on Linux
            result = subprocess.run(
                ["ufw", "status"], 
                capture_output=True, 
                text=True
            )
            return {"status": "active" if "active" in result.stdout.lower() else "inactive"}
        except Exception as e:
            return {"status": "unknown", "error": str(e)}
            
    elif system == "darwin":  # macOS
        try:
            # Check macOS firewall status
            result = subprocess.run(
                ["defaults", "read", "/Library/Preferences/com.apple.alf", "globalstate"],
                capture_output=True,
                text=True
            )
            return {"status": "active" if result.stdout.strip() != "0" else "inactive"}
        except Exception as e:
            return {"status": "unknown", "error": str(e)}
    
    return {"status": "unknown", "error": "Unsupported operating system"}