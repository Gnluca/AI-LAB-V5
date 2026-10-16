@echo off

echo ==========================
echo AI LAB V6
echo ==========================

start "AI SERVER" cmd /k "cd /d E:\AI-Server\server && python app.py"

timeout /t 5 > nul

start "DASHBOARD" cmd /k "cd /d E:\AI-Server\dashboard && streamlit run app.py"

exit