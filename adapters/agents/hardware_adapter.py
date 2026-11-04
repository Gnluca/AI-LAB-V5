import psutil
from datetime import datetime


class HardwareAdapter:

    def run(self, task):

        return {
            "task": task,
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat(),

            "cpu": psutil.cpu_percent(
                interval=1
            ),

            "ram": psutil.virtual_memory().percent,

            "disk": psutil.disk_usage(
                "E:\\"
            ).percent
        }


hardware_adapter = HardwareAdapter()