@echo off
title AI LAB V6

echo ====================================
echo      AVVIO AI LAB V6
echo ====================================

cd /d E:\AI-Server\server

echo.
echo [1/3] Avvio AI Server...
start "AI SERVER" cmd /k "uvicorn server:app --host 0.0.0.0 --port 8000"

timeout /t 5 > nul

echo.
echo [2/3] Verifica servizi...
start http://127.0.0.1:8000/docs

echo.
echo [3/3] Avvio Dashboard...
cd /d E:\AI-Learning-Studio
start "DASHBOARD" cmd /k "python dashboard.py"

echo.
echo AI LAB V6 AVVIATO
pause