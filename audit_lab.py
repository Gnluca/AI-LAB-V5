# audit_lab.py

from pathlib import Path
from datetime import datetime

root = Path("E:/AI-Server")

files = []

for f in root.rglob("*"):
    if f.is_file():
        files.append({
            "file": str(f),
            "modified": datetime.fromtimestamp(f.stat().st_mtime),
            "size": f.stat().st_size
        })

files.sort(key=lambda x: x["modified"])

print("\n=== 50 FILE PIU VECCHI ===\n")

for item in files[:50]:
    print(
        item["modified"].strftime("%Y-%m-%d %H:%M"),
        item["size"],
        item["file"]
    )