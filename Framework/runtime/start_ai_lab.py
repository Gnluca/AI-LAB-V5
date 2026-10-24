import subprocess
import time
import webbrowser

print("Avvio AI LAB V6.2...")

subprocess.Popen(
    [
        "python",
        "-m",
        "uvicorn",
        "server:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
    ],
    cwd=r"E:\AI-Server\server"
)

time.sleep(5)

webbrowser.open(
    r"file:///E:/AI-Server/webui/index.html"
)

print("AI LAB avviato")

while True:
    time.sleep(60)
