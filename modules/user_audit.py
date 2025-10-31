import platform
import subprocess
import os

# Import pwd only on Unix-like systems
try:
    import pwd
    HAVE_PWD = True
except ImportError:
    HAVE_PWD = False

def get_user_accounts():
    """Get list of user accounts and their properties."""
    system = platform.system().lower()
    users = []
    
    if system == "windows":
        try:
            # Using PowerShell to get user account information
            cmd = ["powershell", "-Command", "Get-LocalUser | Select-Object Name,Enabled,LastLogon,PasswordRequired"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            for line in result.stdout.split('\n'):
                if line.strip() and not line.startswith("Name"):
                    parts = line.split()
                    if parts:
                        users.append({
                            "username": parts[0],
                            "enabled": "True" in line,
                            "requires_password": "True" in line
                        })
            return {"status": "success", "users": users}
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    elif system in ["linux", "darwin"] and HAVE_PWD:
        try:
            # Get users from /etc/passwd
            for user in pwd.getpwall():
                if user.pw_uid >= 1000 or user.pw_name in ['root']:  # Regular users and root
                    users.append({
                        "username": user.pw_name,
                        "uid": user.pw_uid,
                        "home": user.pw_dir,
                        "shell": user.pw_shell,
                        "enabled": True  # Assuming enabled if listed
                    })
            return {"status": "success", "users": users}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    elif system in ["linux", "darwin"]:
        try:
            # Alternative method for systems without pwd module
            result = subprocess.run(["cat", "/etc/passwd"], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if line:
                    parts = line.split(':')
                    if len(parts) >= 7:
                        if int(parts[2]) >= 1000 or parts[0] == 'root':
                            users.append({
                                "username": parts[0],
                                "uid": int(parts[2]),
                                "home": parts[5],
                                "shell": parts[6],
                                "enabled": True
                            })
            return {"status": "success", "users": users}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    return {"status": "unknown", "error": "Unsupported operating system"}