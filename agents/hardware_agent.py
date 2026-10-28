"""Hardware metrics agent with optional psutil support."""
import os
import platform
from agents.base_agent import BaseAgent

try:
    import psutil
except ImportError:  # Optional dependency: keep the lab bootable.
    psutil = None


class HardwareAgent(BaseAgent):
    def __init__(self):
        super().__init__("HardwareAgent")

    def run(self):
        if psutil is None:
            return {"hostname": platform.node(), "cpu": None, "ram": None, "degraded": True}
        return {
            "hostname": platform.node(),
            "cpu": psutil.cpu_percent(interval=0.1),
            "ram": psutil.virtual_memory().percent,
            "degraded": False,
        }

    status = run
