"""Connectivity smoke test; a remote node being offline is reported, not raised."""
import os
import requests

URL = os.getenv("AI_LAB_NODE56_URL", "http://192.168.1.56:8000/status")
TIMEOUT = float(os.getenv("AI_LAB_NODE_TIMEOUT", "3"))


def check_node(url: str = URL) -> dict:
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        payload = response.json()
        return {"reachable": True, "status_code": response.status_code, "payload": payload}
    except (requests.RequestException, ValueError) as exc:
        return {"reachable": False, "error": str(exc)}


if __name__ == "__main__":
    result = check_node()
    print(result)
    raise SystemExit(0)
