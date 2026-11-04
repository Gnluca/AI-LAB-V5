import os
import requests

class NodeProvider:
    def __init__(self, base_url=None, timeout=None, session=None):
        self.base_url = (base_url or os.getenv("AI_LAB_NODE56_URL", "http://192.168.1.56:8000")).rstrip("/")
        self.timeout = float(timeout if timeout is not None else os.getenv("AI_LAB_NODE_TIMEOUT", "3"))
        self.session = session or requests

    def collect(self):
        try:
            response = self.session.get(f"{self.base_url}/status", timeout=self.timeout)
            if response.ok:
                try: details = response.json()
                except (ValueError, AttributeError): details = {}
                return {"resource": "node56", "status": "online", "endpoint": self.base_url,
                        "details": details if isinstance(details, dict) else {}}
            return {"resource": "node56", "status": "offline", "endpoint": self.base_url,
                    "http_status": response.status_code}
        except requests.RequestException as exc:
            return {"resource": "node56", "status": "offline", "endpoint": self.base_url,
                    "error": str(exc)}

node_provider = NodeProvider()
