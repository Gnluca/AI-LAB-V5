import psutil


class CpuProvider:

    def collect(self):

        usage = psutil.cpu_percent(interval=1)

        if usage > 90:
            status = "critical"
        elif usage > 70:
            status = "warning"
        else:
            status = "healthy"

        return {
            "resource": "cpu",
            "usage": usage,
            "status": status
        }


cpu_provider = CpuProvider()