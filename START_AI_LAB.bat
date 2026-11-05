@echo off
cd /d E:\AI-Server

start "AI-LAB SERVER" cmd /k python -m uvicorn server.server:app --host 0.0.0.0 --port 8000

timeout /t 5 >nul

start "AI-LAB RUNTIME" cmd /k python runtime\ai_lab_runtime.py

timeout /t 10 >nul

python diagnostics.py > data\logs\diagnostics_startup.log 2>&1

exit