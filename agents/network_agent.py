from agents.base_agent import BaseAgent

class NetworkAgent(BaseAgent):

    def __init__(self):
        super().__init__("NetworkAgent")

    def run(self):

        return {
            "network": "ok"
        }