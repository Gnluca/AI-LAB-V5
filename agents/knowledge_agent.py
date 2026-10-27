from agents.base_agent import BaseAgent

class KnowledgeAgent(BaseAgent):

    def __init__(self):
        super().__init__("KnowledgeAgent")

    def run(self):

        return {
            "knowledge": "updated"
        }