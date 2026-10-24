from datetime import datetime
import requests
import uvicorn
import sys

# Percorso del server FastAPI
sys.path.insert(0, r"E:\AI-Server\server")

# Import applicazione FastAPI
from server import app

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


if __name__ == "__main__":

    banner()

    startup_checks()

    print()
    print("Starting AI-LAB API...")
    print()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
     
hiddenimports=[
    "sqlite3"
]     