"""Portable AI-LAB launcher."""
from pathlib import Path
import os
import subprocess
import sys


def main() -> int:
    root = Path(__file__).resolve().parent
    runtime = root / "runtime" / "AI-LAB-Runtime.py"
    if not runtime.exists():
        raise FileNotFoundError(f"Runtime not found: {runtime}")
    command = [sys.executable, str(runtime)]
    kwargs = {"cwd": str(root)}
    if os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    return subprocess.call(command, **kwargs)


if __name__ == "__main__":
    raise SystemExit(main())
