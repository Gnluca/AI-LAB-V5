import platform
import psutil

class HardwareAgent:

    def status(self):

        return {
            "hostname": platform.node(),
            "cpu_cores": psutil.cpu_count(),
            "ram_gb": round(
                psutil.virtual_memory().total /
                1024**3,
                2
            ),
            "disk_free_gb": round(
                psutil.disk_usage("C:\\").free /
                1024**3,
                2
            )
        }