import requests

NODES = {
    "NODE41": "localhost",
    "NODE56": "192.168.1.56"
}


def network_status():

    results = {}

    for node, host in NODES.items():

        try:

            requests.get(
                f"http://{host}:8000/status",
                timeout=3
            )

            results[node] = "ONLINE"

        except:

            results[node] = "OFFLINE"

    return results


if __name__ == "__main__":

    print()
    print("NETWORK STATUS")
    print("-" * 30)

    for node, status in network_status().items():
        print(f"{node:<10} {status}")