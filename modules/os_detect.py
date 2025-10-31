import platform

def get_os_info():
    return platform.system(), platform.release()

if __name__ == "__main__":
    os_name, os_version = get_os_info()
    print(f"Operating System: {os_name}, Version: {os_version}")
# This script detects the operating system and its version using the platform module.