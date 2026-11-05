import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

VERSION_FILE = BASE_DIR / "deployment" / "version.json"


def get_version():
    if not VERSION_FILE.exists():
        return {
            "application": "AI-LAB",
            "version": "7.0.0",
            "build": "2026.11.05"
        }

    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_version(version_data):
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump(version_data, f, indent=2)