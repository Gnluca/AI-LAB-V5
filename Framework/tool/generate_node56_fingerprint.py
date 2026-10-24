import json
import socket
import platform
import psutil
from datetime import datetime

hostname = socket.gethostname()

try:
    ip_address = socket.gethostbyname(hostname)
except:
    ip_address = "unknown"

fingerprint = {
    "node_id": "node56",
    "hostname": hostname,
    "role": "secondary",
    "environment": "AI-LAB",
    "version": "V6.2",
    "ip_address": ip_address,
    "subnet": "255.255.255.0",
    "gateway": "192.168.1.33",
    "managed_by": "node41",
    "primary_node": "192.168.1.41",
    "operating_system": platform.system(),
    "os_version": platform.version(),
    "python_version": platform.python_version(),
    "cpu_cores": psutil.cpu_count(logical=False),
    "logical_cores": psutil.cpu_count(logical=True),
    "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
    "status": "online",
    "governed": True,
    "registered": True,
    "generated": datetime.now().isoformat()
}

with open(
    r"E:\AI-Server\Framework\config\node56_fingerprint.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(fingerprint, f, indent=4)

print("NODE56 fingerprint generata")