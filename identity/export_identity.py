from pathlib import Path
import shutil

SOURCE = Path(r"E:\AI-Server\identity")
TARGET = Path(r"\\192.168.1.56\AI-LAB-Identity")

TARGET.mkdir(parents=True, exist_ok=True)

for file in SOURCE.iterdir():
    if file.is_file():
        shutil.copy2(file, TARGET)

print("Identity esportata al Nodo56")