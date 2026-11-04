from datetime import datetime
import requests


class ServiceAdapter:

    def run(self, task):

        services = {
            "api": False,
            "ollama": False
        }

        try:

            r = requests.get(
                "http://127.0.0.1:8000/status",
                timeout=3
            )

            services["api"] = (
                r.status_code == 200
            )

        except Exception:
            pass

        try:

            r = requests.get(
                "http://127.0.0.1:11434/api/tags",
                timeout=3
            )

            services["ollama"] = (
                r.status_code == 200
            )

        except Exception:
            pass

        return {
            "task": task,
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat(),
            "services": services
        }


service_adapter = ServiceAdapter()