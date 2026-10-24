import json
from pathlib import Path

REGISTRY_DIR = Path("registry")


def load_registry():

    file = REGISTRY_DIR / "registry.json"

    if not file.exists():
        return {}

    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_registry(data):

    REGISTRY_DIR.mkdir(exist_ok=True)

    with open(
        REGISTRY_DIR / "registry.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":

    registry = load_registry()

    print(json.dumps(
        registry,
        indent=4
    ))