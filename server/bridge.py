import requests

OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "llama3.1"


def generate(prompt, model=DEFAULT_MODEL):

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 2048
        }
    }

    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload
    )

    return r.json()


def server_status():

    try:

        r = requests.get(
            f"{OLLAMA_URL}/api/tags"
        )

        if r.status_code == 200:

            return {
                "status": "online",
                "ollama": "online",
                "model": DEFAULT_MODEL
            }

    except Exception:

        pass

    return {
        "status": "offline",
        "ollama": "offline",
        "model": DEFAULT_MODEL
    }


def list_models():

    r = requests.get(
        f"{OLLAMA_URL}/api/tags"
    )

    return r.json()