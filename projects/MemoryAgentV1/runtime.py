import requests

SERVER = "http://127.0.0.1:8000"


class MemoryAgent:

    def __init__(self):

        self.name = "MemoryAgentV1"

    def build_snapshot(self):

        memory = requests.get(
            f"{SERVER}/memory/list"
        ).json()

        factory = requests.get(
            f"{SERVER}/factory/status"
        ).json()

        network = requests.get(
            f"{SERVER}/network/lab"
        ).json()

        snapshot = {
            "memory_records": memory["count"],
            "agents": factory["agents"],
            "primary_node": factory["primary_node"],
            "legacy_node": factory["legacy_node"],
            "model": factory["model"],
            "laboratory": network["laboratory"]
        }

        return snapshot


if __name__ == "__main__":

    agent = MemoryAgent()

    print(
        agent.build_snapshot()
    )