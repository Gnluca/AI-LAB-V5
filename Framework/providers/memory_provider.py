import psutil


class MemoryProvider:

    def collect(self):

        mem = psutil.virtual_memory()

        return {
            "resource": "ram",
            "usage": mem.percent,
            "total_gb": round(mem.total / 1024**3, 2),
            "available_gb": round(mem.available / 1024**3, 2)
        }


memory_provider = MemoryProvider()