import subprocess
import time
import webbrowser

print("Avvio AI LAB V6.2...")

# FastAPI
subprocess.Popen(
    ["python", "-m", "uvicorn", "server:app",
     "--host", "0.0.0.0", "--port", "8000"],
    cwd=r"E:\AI-Server\server"
)

# Attesa avvio
time.sleep(5)

# Dashboard
webbrowser.open("http://localhost:8080/index.html")

print("AI LAB avviato")
input("Premi INVIO per chiudere...")