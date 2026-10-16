@echo off

start "MANAGER" cmd /k "cd /d E:\AI-Server\manager && python manager.py"

timeout /t 15

start http://localhost:8080/index.html

exit