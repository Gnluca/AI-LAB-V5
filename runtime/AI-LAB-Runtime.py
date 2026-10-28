"""AI-LAB runtime entry point."""
from __future__ import annotations

import os
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
import uvicorn

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.app import app  # noqa: E402


def port_in_use(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


def check_ollama() -> bool:
    url = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
    try:
        return requests.get(f"{url}/api/tags", timeout=3).status_code == 200
    except requests.RequestException:
        return False


def startup_checks() -> dict:
    state = {"runtime": True, "ollama": check_ollama(), "started_at": datetime.now(timezone.utc).isoformat()}
    print(f"[OK] Runtime | Ollama: {'online' if state['ollama'] else 'offline'}")
    return state


def main() -> int:
    host = os.getenv("AI_LAB_HOST", "0.0.0.0")
    port = int(os.getenv("AI_LAB_PORT", "8000"))
    if port_in_use("127.0.0.1", port):
        print(f"[INFO] AI-LAB già avviato sulla porta {port}")
        return 0
    print(f"AI-LAB runtime avviato: {datetime.now(timezone.utc).isoformat()}")
    startup_checks()
    uvicorn.run(app, host=host, port=port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
