@echo off
title AI LAB V6 SERVER

cd /d E:\AI-Server\server

echo ============================
echo AVVIO AI LAB V6
echo ============================

uvicorn server:app --host 0.0.0.0 --port 8000

pause