from datetime import datetime
import requests
import uvicorn
import socket
import sys
import os

ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

MCP = os.path.join(
    ROOT,
    "projects",
    "MCP"
)

for p in [ROOT, MCP]:
    if p not in sys.path:
        sys.path.insert(0, p)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if sock.connect_ex(("127.0.0.1", 8000)) == 0:
    print("[INFO] AI-LAB già avviato sulla porta 8000")
    sys.exit(0)

# Import applicazione FastAPI
# ROOT è già inserito nel sys.path sopra

from server.server import app
import threading

import importlib.util

MASTER_LOOP_PATH = os.path.join(
    ROOT,
    "runtime",
    "master_loop.py"
)

spec = importlib.util.spec_from_file_location(
    "master_loop",
    MASTER_LOOP_PATH
)

master_loop_module = importlib.util.module_from_spec(spec)

spec.loader.exec_module(master_loop_module)

MasterLoop = master_loop_module.MasterLoop

LAB_STATUS = {
    "runtime": False,
    "ollama": False
}


def banner():

    print("=" * 60)
    print("AI-LAB RUNTIME v6.3")
    print("=" * 60)
    print(f"Boot Time : {datetime.now()}")
    print("=" * 60)


def check_ollama():

    try:

        r = requests.get(
            "http://localhost:11434/api/tags",
            timeout=3
        )

        if r.status_code == 200:

            LAB_STATUS["ollama"] = True

            print("[OK] Ollama")

        else:

            print("[WARN] Ollama")

    except Exception as e:

        print(f"[WARN] Ollama : {e}")


def startup_checks():

    LAB_STATUS["runtime"] = True

    print("[OK] Runtime")

    check_ollama()

    print()

    if all(LAB_STATUS.values()):

        print("[ONLINE] AI-LAB READY")

    else:

        print("[DEGRADED] AI-LAB")
        
def start_master_loop():

    try:

        loop = MasterLoop()

        loop.run()

    except Exception as e:

        print(
            f"[MASTER LOOP ERROR] {e}"
        )        


if __name__ == "__main__":

    banner()

    startup_checks()

    print()
    print("Starting Master Loop...")
    print()

    threading.Thread(
        target=start_master_loop,
        daemon=True
    ).start()

    print("Starting AI-LAB API...")
    print()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
         