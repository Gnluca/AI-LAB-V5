from pathlib import Path
import shutil
from datetime import datetime

# Sorgenti Nodo41

SOURCES = [
    Path(r"E:\AI-Server\identity"),
    Path(r"E:\AI-Server\passport"),
    Path(r"E:\AI-Server\registry")
]

# Destinazione Nodo56 (share di rete)

DESTINATION = Path(r"\\192.168.1.56\AI-Server-Sync")

LOGFILE = Path(r"E:\AI-Server\runtime\sync.log")


def log(message):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = f"[{timestamp}] {message}"

    print(line)

    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def sync_folder(source, destination):

    if not source.exists():
        log(f"Cartella non trovata: {source}")
        return

    target = destination / source.name

    target.mkdir(parents=True, exist_ok=True)

    for item in source.rglob("*"):

        if item.is_file():

            relative_path = item.relative_to(source)

            destination_file = target / relative_path

            destination_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            shutil.copy2(
                item,
                destination_file
            )

            log(f"Copiato: {item.name}")


def main():

    log("=" * 60)
    log("AI-LAB NODE SYNC")
    log("=" * 60)

    if not DESTINATION.exists():

        try:
            DESTINATION.mkdir(
                parents=True,
                exist_ok=True
            )
        except Exception as e:

            log(f"Nodo56 non raggiungibile: {e}")
            return

    for folder in SOURCES:
        sync_folder(
            folder,
            DESTINATION
        )

    log("SINCRONIZZAZIONE COMPLETATA")


if __name__ == "__main__":
    main()