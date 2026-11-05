import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INCLUDE = [
    "adapters",
    "agenda",
    "agents",
    "cognitive_core",
    "config",
    "core",
    "events",
    "framework",
    "governance",
    "identity",
    "knowledge",
    "manager",
    "projects",
    "runtime",
    "scheduler",
    "security",
    "server",
    "webui",
    "registry"
]

EXCLUDE = [
    "__pycache__",
    ".git",
    ".venv",
    "build",
    "tests",
    "backups",
    "packages",
    "webui_backup"
]


def should_skip(path_str):
    path_str = path_str.lower()

    for item in EXCLUDE:
        if item.lower() in path_str:
            return True

    return False


def build_package(version="7.0.0"):

    packages_dir = BASE_DIR / "packages"
    packages_dir.mkdir(exist_ok=True)

    zip_file = packages_dir / f"AI-LAB-{version}.zip"

    with zipfile.ZipFile(
        zip_file,
        "w",
        zipfile.ZIP_DEFLATED
    ) as archive:

        for folder in INCLUDE:

            src = BASE_DIR / folder

            if not src.exists():
                continue

            for file in src.rglob("*"):

                if not file.is_file():
                    continue

                if should_skip(str(file)):
                    continue

                archive.write(
                    file,
                    file.relative_to(BASE_DIR)
                )

    return zip_file


if __name__ == "__main__":

    result = build_package()

    print()
    print("PACKAGE CREATED")
    print(result)
    print()