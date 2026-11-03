import requests


class NodeProvider:

    def collect(self):

        try:

            response = requests.get(
                "http://127.0.0.1:8000/status",
                timeout=5
            )

            if response.status_code == 200:

                return {
                    "resource": "node56",
                    "status": "online"
                }

        except Exception:

            pass

        return {
            "resource": "node56",
            "status": "offline"
        }


node_provider = NodeProvider()