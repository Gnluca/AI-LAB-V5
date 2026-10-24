import requests

NODES = {
    "NODE41": "localhost",
    "NODE56": "192.168.1.56"
}


def check_node(name, host):

    try:

        r = requests.get(
            f"http://{host}:8000/status",
            timeout=3
        )

        data = r.json()

        print()
        print(f"{name}")
        print(f"STATUS : {data.get('status')}")
        print(f"MODEL  : {data.get('model')}")

    except:

        print(f"{name} OFFLINE")


if __name__ == "__main__":

    print("AI-LAB NODE SYNC")

    for name, host in NODES.items():
        check_node(name, host)