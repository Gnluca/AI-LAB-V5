import json
from pathlib import Path
from settings import NODES
from settings import *


for node, ip in NODES.items():
    print(node, ip)


def generate_passport(
    node_id,
    hostname,
    ip,
    role
):

    data = {
        "node_id": node_id,
        "hostname": hostname,
        "ip": ip,
        "role": role,
        "status": "ONLINE",
        "runtime": "6.2"
    }

    Path("registry").mkdir(exist_ok=True)

    file = Path("registry") / f"{node_id.lower()}.json"

    with open(
        file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=4
        )

    print("Passaporto creato:", file)


if __name__ == "__main__":

    generate_passport(
        "NODE41",
        "AI-LAB-PRIMARY",
        "192.168.1.41",
        "PRIMARY"
    )