@echo off

start "FASTAPI" cmd /k "cd /d E:\AI-Server\server && python app.py"

timeout /t 5 > nul

start "WEBUI" cmd /k "cd /d E:\AI-Server\webui && python -m http.server 8080"

timeout /t 2 > nul

start "" http://localhost:8080/index.html
