import platform
from datetime import datetime
import json
from pathlib import Path

def get_os_info():
    return platform.system(), platform.release()

def save_audit_log(data):
    exports_dir = Path(__file__).parent.parent / 'exports'
    exports_dir.mkdir(exist_ok=True)
    
    # Save JSON log
    json_file = exports_dir / f"audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)

    # Save MD log
    md_file = exports_dir / f"audit_log_{datetime.now().strftime('%Y%m%d')}.md"
    with open(md_file, "w") as f:
        f.write("# NEXUM-CHECKPOINT Audit Log\n")
        f.write(f"Scan Date: {datetime.now()}\n")
        f.write("\n## System Information\n")
        os_name, os_version = get_os_info()
        f.write(f"- Operating System: {os_name}\n")
        f.write(f"- OS Version: {os_version}\n")

if __name__ == "__main__":
    os_name, os_version = get_os_info()
    print(f"Operating System: {os_name}, Version: {os_version}")
    
    # Test audit log creation
    test_data = {
        "os": get_os_info(),
        "timestamp": datetime.now().isoformat()
    }
    save_audit_log(test_data)