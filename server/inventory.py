from pathlib import Path


ROOT = Path(r"E:\AI-Server")


def scan_inventory():

    files = 0

    for _ in ROOT.rglob("*"):
        files += 1

    return {
        "root": str(ROOT),
        "total_files": files,
        "status": "online"
    }