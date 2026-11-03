import json
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FRAMEWORK_DIR = BASE_DIR / "framework"

if str(FRAMEWORK_DIR) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_DIR))

from resource_manager import resource_manager


def build_observation():

    resources = resource_manager.collect()

    observation = {
        "timestamp": datetime.now().isoformat(),
        "node41": "online",
        "node56": resources["node56"]["status"],

        "cpu": resources["cpu"],
        "memory": resources["memory"],
        "ollama": resources["ollama"],

        "alerts": []
    }

    return observation


if __name__ == "__main__":

    print(
        json.dumps(
            build_observation(),
            indent=4
        )
    )