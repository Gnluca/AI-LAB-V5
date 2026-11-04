import requests
from datetime import datetime


class NetworkAdapter:

    def run(self, task):

        node56 = "offline"

        try:

            response = requests.get(
                "http://127.0.0.1:8000/status",
                timeout=3
            )

            if response.status_code == 200:
                node56 = "online"

        except Exception:
            pass

        return {
            "task": task,
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat(),
            "node56": node56
        }


network_adapter = NetworkAdapter()