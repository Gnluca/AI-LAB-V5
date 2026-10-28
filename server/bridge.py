"""Small, bounded-time client for the local Ollama service."""
import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "10"))


def generate(prompt: str, model: str = DEFAULT_MODEL) -> dict:
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False, "options": {"num_ctx": 2048}},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, dict) else {"response": str(data)}


def server_status() -> dict:
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        response.raise_for_status()
        models = response.json().get("models", [])
        names = [item.get("name") for item in models if isinstance(item, dict) and item.get("name")]
        return {"status": "online", "ollama": "online", "model": names[0] if names else DEFAULT_MODEL}
    except (requests.RequestException, ValueError, TypeError):
        return {"status": "degraded", "ollama": "offline", "model": DEFAULT_MODEL}


def list_models() -> dict:
    response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, dict) else {"models": []}
