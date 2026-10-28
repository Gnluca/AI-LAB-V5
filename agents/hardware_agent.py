import psutil

from agents.base_agent import BaseAgent

class HardwareAgent(BaseAgent):

    def __init__(self):
        super().__init__("HardwareAgent")

    def run(self):

        return {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent
        }