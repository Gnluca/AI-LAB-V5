import requests
import subprocess
import os
import time

OLLAMA_URL = "http://127.0.0.1:11434/api/tags"
FASTAPI_URL = "http://127.0.0.1:8000"


def online(url):
    try:
        requests.get(url, timeout=3)
        return True
    except:
        return False


def start_ollama():

    print("Avvio Ollama...")

    subprocess.Popen(
        [
            r"C:\Users\lucaa\AppData\Local\Programs\Ollama\Ollama.exe",
            "serve"
        ]
    )


def start_fastapi():

    print("Avvio FastAPI...")

    subprocess.Popen(
        'cd /d E:\\AI-Server\\server && uvicorn server:app --host 0.0.0.0 --port 8000',
        shell=True
    )


while True:

    if not online(OLLAMA_URL):
        start_ollama()
        time.sleep(10)

    if not online(FASTAPI_URL):
        start_fastapi()
        time.sleep(5)

    print("Sistema OK")
    time.sleep(30)
    
    
    OLLAMA_URL = "http://127.0.0.1:11434/api/tags"

if not online(OLLAMA_URL):
    start_ollama()
else:
    print("Ollama già attivo")