@echo off

start "AI SERVER" cmd /k "cd /d E:\AI-Server\server && uvicorn server:app --host 0.0.0.0 --port 8000"

timeout /t 5 > nul

start "DASHBOARD" cmd /k "cd /d E:\AI-Learning-Studio && python dashboard.py"