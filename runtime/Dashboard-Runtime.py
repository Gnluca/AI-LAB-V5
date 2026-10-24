import subprocess
import os

DASHBOARD_PATH = r"E:\AI-Learning-Studio\app\dashboard.py"

print("AI-LAB Dashboard Runtime")

if os.path.exists(DASHBOARD_PATH):
    subprocess.run(["python", DASHBOARD_PATH])
else:
    print("Dashboard non trovata")