import psutil
from datetime import datetime


class MemoryAdapter:

    def run(self, task):

        memory = psutil.virtual_memory()

        return {
            "task": task,
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat(),

            "ram_usage": memory.percent,
            "available_gb": round(
                memory.available / (1024 ** 3),
                2
            ),

            "total_gb": round(
                memory.total / (1024 ** 3),
                2
            )
        }


memory_adapter = MemoryAdapter()