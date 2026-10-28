"""Resilient orchestration loop for AI-LAB agents."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
STATUS_FILE = DATA_DIR / "loop_status.json"
LOG_FILE = DATA_DIR / "master_loop.log"

# Optional agents must not prevent the runtime from starting.
sys.path.insert(0, str(BASE_DIR / "projects" / "NetworkAgent"))
sys.path.insert(0, str(BASE_DIR / "projects" / "HardwareAgent"))

try:
    from network_agent import NetworkAgent
except Exception:
    NetworkAgent = None  # type: ignore[assignment,misc]

try:
    from hardware_agent import HardwareAgent
except Exception:
    HardwareAgent = None  # type: ignore[assignment,misc]

try:
    from event_agent import EventAgent
except Exception:
    EventAgent = None  # type: ignore[assignment,misc]


class MasterLoop:
    def __init__(self, status_file: Path = STATUS_FILE, log_file: Path = LOG_FILE):
        self.cycles = 0
        self.start_time = datetime.now(timezone.utc)
        self.status_file = Path(status_file)
        self.log_file = Path(log_file)
        self.network = NetworkAgent() if NetworkAgent else None
        self.hardware = HardwareAgent() if HardwareAgent else None
        self.events = EventAgent() if EventAgent else None

    def log(self, message: str) -> None:
        line = f"[{datetime.now(timezone.utc).isoformat()}] {message}"
        print(line)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with self.log_file.open("a", encoding="utf-8") as stream:
            stream.write(line + "\n")

    @staticmethod
    def _call(agent: Any, method_names: tuple[str, ...], default: Any) -> Any:
        if agent is None:
            return default
        for name in method_names:
            method = getattr(agent, name, None)
            if callable(method):
                try:
                    return method()
                except Exception:
                    return default
        return default

    def run_network(self) -> dict[str, Any]:
        value = self._call(self.network, ("status", "run"), {"available": False})
        return value if isinstance(value, dict) else {"available": False, "value": value}

    def run_hardware(self) -> dict[str, Any]:
        value = self._call(self.hardware, ("status", "run"), {"available": False})
        return value if isinstance(value, dict) else {"available": False, "value": value}

    def run_events(self) -> list[Any]:
        value = self._call(self.events, ("recent_events", "run"), [])
        return value if isinstance(value, list) else []

    def save_status(self, network: dict[str, Any], hardware: dict[str, Any], events: list[Any]) -> dict[str, Any]:
        nodes_online = sum(1 for value in network.values() if value is True or value == "online")
        status = {
            "status": "online",
            "cycle": self.cycles,
            "started_at": self.start_time.isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "nodes_online": nodes_online,
            "network": network,
            "hardware": hardware,
            "events": events,
        }
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.status_file.with_suffix(self.status_file.suffix + ".tmp")
        temporary.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")
        temporary.replace(self.status_file)
        return status

    def run_once(self) -> dict[str, Any]:
        self.cycles += 1
        network = self.run_network()
        hardware = self.run_hardware()
        events = self.run_events()
        return self.save_status(network, hardware, events)

    def run_forever(self, interval: float = 30.0) -> None:
        import time
        while True:
            try:
                self.run_once()
            except Exception as exc:
                self.log(f"MasterLoop error: {exc}")
            time.sleep(max(0.1, interval))


if __name__ == "__main__":
    MasterLoop().run_forever()
