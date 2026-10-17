from pathlib import Path

ROOT = Path("E:/AI-Server")

for file in ROOT.rglob("*.py"):
    print(file)