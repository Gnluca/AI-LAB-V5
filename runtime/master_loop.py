import json
import time
import traceback
from pathlib import Path
from datetime import datetime
import sys

# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(r"E:\AI-Server")

STATUS_FILE = BASE_DIR / "data" / "loop_status.json"
LOG_FILE = BASE_DIR / "data" / "master_loop.log"

# ==========================================
# IMPORT AGENTS
# ==========================================

sys.path.append(str(BASE_DIR / "projects" / "NetworkAgent"))
sys.path.append(str(BASE_DIR / "projects" / "HardwareAgent"))

NETWORK_AVAILABLE = False
HARDWARE_AVAILABLE = False
EVENT_AVAILABLE = False

try:
    from network_agent import NetworkAgent

    NETWORK_AVAILABLE = True

except Exception as e:
    print(f"[WARN] NetworkAgent not loaded: {e}")

try:
    from hardware_agent import HardwareAgent

    HARDWARE_AVAILABLE = True

except Exception as e:
    print(f"[WARN] HardwareAgent not loaded: {e}")

try:
    from event_agent import EventAgent

    EVENT_AVAILABLE = True

except Exception as e:
    print(f"[WARN] EventAgent not loaded: {e}")

# ==========================================
# MASTER LOOP
# ==========================================


class MasterLoop:

    def __init__(self):

        self.cycles = 0
        self.start_time = datetime.now()

        self.network = None
        self.hardware = None
        self.events = None

        if NETWORK_AVAILABLE:
            self.network = NetworkAgent()

        if HARDWARE_AVAILABLE:
            self.hardware = HardwareAgent()

        if EVENT_AVAILABLE:
            self.events = EventAgent()

    # --------------------------------------

    def log(self, message):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        line = f"[{timestamp}] {message}"

        print(line)

        LOG_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(line + "\n")

    # --------------------------------------

    def run_network(self):

        if not self.network:
            return {"available": False}

        try:
            return self.network.status()

        except Exception as e:

            self.log(
                f"NetworkAgent Error: {e}"
            )

            return {
                "available": False,
                "error": str(e)
            }

    # --------------------------------------

    def run_hardware(self):

        if not self.hardware:
            return {"available": False}

        try:
            return self.hardware.status()

        except Exception as e:

            self.log(
                f"HardwareAgent Error: {e}"
            )

            return {
                "available": False,
                "error": str(e)
            }

    # --------------------------------------

    def run_events(self):

        if not self.events:
            return []

        try:
            return self.events.recent_events()

        except Exception as e:

            self.log(
                f"EventAgent Error: {e}"
            )

            return []

    # --------------------------------------

    def save_status(
        self,
        network,
        hardware,
        events
    ):

        try:

            nodes_online = 0

            if isinstance(network, dict):

                nodes_online = sum(
                    1
                    for value in network.values()
              