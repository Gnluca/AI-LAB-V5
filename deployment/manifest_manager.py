import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

PACKAGE_DIR = BASE_DIR / "packages"


def create_manifest(version="7.0.0"):

    PACKAGE_DIR.mkdir(exist_ok=True)

    manifest = {
        "application": "AI-LAB",
        "version": version,
        "build": datetime.now().strftime("%Y.%m.%d"),
        "created_by": "node41",
        "python": "3.14"
    }

    manifest_file = PACKAGE_DIR / "manifest.json"

    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return manifest