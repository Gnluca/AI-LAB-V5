@echo off

start "OLLAMA" cmd /k "\"C:\Users\lucaa\AppData\Local\Programs\Ollama\ollama.exe\" serve"

timeout /t 10

start "FASTAPI" cmd /k "cd /d E:\AI-Server\server && uvicorn server:app --host 0.0.0.0 --port 8000"

timeout /t 5

start "STREAMLIT" cmd /k "cd /d E:\AI-Server\client && streamlit run app.py --server.port 8505"

timeout /t 15

start http://localhost:8505

exit