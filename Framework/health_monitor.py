import json
import psutil
import requests
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"E:\AI-Server")
OUTPUT_FILE = BASE_DIR / "data" / "health_status.json"


def check_ollama():
    try:
        r = requests.get(
            "http://127.0.0.1:11434/api/tags",
            timeout=3
        )

        if r.status_code == 200:
            return "online"

    except Exception:
        pass

    return "offline"


def check_node56():
    try:
        r = requests.get(
            "http://192.168.1.56:8000/status",
            timeout=3
        )

        if r.status_code == 200:
            return "online"

    except Exception:
        pass

    return "offline"


def build_health_report():

    report = {
        "timestamp": datetime.now().isoformat(),
        "fastapi": "online",
        "ollama": check_ollama(),
        "node41": "online",
        "node56": check_node56(),
        "cpu": round(psutil.cpu_percent(), 1),
        "ram": round(psutil.virtual_memory().percent, 1),
        "disk": round(psutil.disk_usage("E:\\").percent, 1)
    }

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            report,
            f,
            indent=2
        )

    return report


if __name__ == "__main__":

    result = build_health_report()

    print(
        json.dumps(
            result,
            indent=2
        )
    )