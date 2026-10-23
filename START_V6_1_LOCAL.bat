@echo off

title AI LAB V6.1 LOCAL

echo =====================================
echo AI LAB V6.1 LOCAL EDITION
echo =====================================

echo.

echo [1/4] Avvio FastAPI...
start "AI-LAB-Server" cmd /k "cd /d E:\AI-Server\server && uvicorn server:app --host 0.0.0.0 --port 8000"

timeout /t 5 >nul

echo [2/4] Verifica API...
powershell -Command "try { Invoke-RestMethod http://127.0.0.1:8000/status | Out-Null; Write-Host 'FASTAPI ONLINE' -ForegroundColor Green } catch { Write-Host 'FASTAPI OFFLINE' -ForegroundColor Red }"

echo.

echo [3/4] Avvio Dashboard Server...
start "Dashboard" cmd /k "cd /d E:\AI-Server\webui && python -m http.server 8080"

timeout /t 2 >nul

start http://localhost:8080

echo.

echo [4/4] Avvio Framework V6.2...
start "AI-LAB-Framework" cmd /k "cd /d E:\AI-Server\Framework && python -m runtime.run_manager"

echo.

echo =====================================
echo AI LAB AVVIATO
echo =====================================

pause