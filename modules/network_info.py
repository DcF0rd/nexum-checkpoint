import platform
import subprocess
import socket
import json

def get_network_info():
    """Get comprehensive network interface information."""
    info = {
        "interfaces": [],
        "hostname": socket.gethostname(),
        "fqdn": socket.getfqdn()
    }
    
    system = platform.system().lower()
    
    if system == "windows":
        try:
            # Get network adapters using PowerShell
            cmd = ["powershell", "-Command", 
                  "Get-NetAdapter | Select-Object Name,Status,MacAddress | ConvertTo-Json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                adapters = json.loads(result.stdout)
                if isinstance(adapters, dict):  # Single adapter
                    adapters = [adapters]
                for adapter in adapters:
                    interface = {
                        "name": adapter["Name"],
                        "status": adapter["Status"].lower(),
                        "mac": adapter["MacAddress"],
                        "addresses": []
                    }
                    
                    # Get IP addresses
                    cmd = ["powershell", "-Command", 
                          f"Get-NetIPAddress -InterfaceAlias '{adapter['Name']}' | Select-Object IPAddress,AddressFamily | ConvertTo-Json"]
                    ip_result = subprocess.run(cmd, capture_output=True, text=True)
                    if ip_result.returncode == 0:
                        try:
                            ips = json.loads(ip_result.stdout)
                            if isinstance(ips, dict):
                                ips = [ips]
                            for ip in ips:
                                if ip["AddressFamily"] == 2:  # IPv4
                                    interface["addresses"].append({
                                        "type": "IPv4",
                                        "addr": ip["IPAddress"]
                                    })
                                elif ip["AddressFamily"] == 23:  # IPv6
                                    interface["addresses"].append({
                                        "type": "IPv6",
                                        "addr": ip["IPAddress"]
                                    })
                        except json.JSONDecodeError:
                            pass
                    
                    info["interfaces"].append(interface)
        except Exception as e:
            info["error"] = str(e)
    else:
        try:
            # Try using 'ip' command first (modern Linux)
            cmd = ["ip", "addr"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            current_interface = None
            for line in result.stdout.split('\n'):
                if not line.startswith(' '):
                    if current_interface:
                        info["interfaces"].append(current_interface)
                    if ':' in line:
                        iface_name = line.split(':')[1].strip()
                        current_interface = {
                            "name": iface_name,
                            "addresses": [],
                            "status": "up" if "UP" in line else "down"
                        }
                elif current_interface:
                    if 'inet ' in line:
                        addr = line.split('inet ')[1].split('/')[0]
                        current_interface["addresses"].append({
                            "type": "IPv4",
                            "addr": addr
                        })
                    elif 'inet6 ' in line:
                        addr = line.split('inet6 ')[1].split('/')[0]
                        current_interface["addresses"].append({
                            "type": "IPv6",
                            "addr": addr
                        })
            
            if current_interface:
                info["interfaces"].append(current_interface)
                
            # Get MAC addresses
            cmd = ["ip", "link"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'link/ether' in line:
                        mac = line.split('link/ether')[1].split()[0]
                        iface_name = line.split(':')[1].strip().split('@')[0]
                        for interface in info["interfaces"]:
                            if interface["name"] == iface_name:
                                interface["mac"] = mac
                                break
        except Exception as e:
            info["error"] = str(e)
    
    return info