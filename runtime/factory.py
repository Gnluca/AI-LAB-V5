class Factory:

    def __init__(self):
        self.agents = {}

    def register(self, agent):
        self.agents[agent.name] = agent

    def get(self, name):
        return self.agents.get(name)

    def status(self):
        return {
            "registered": len(self.agents),
            "agents": list(self.agents.keys())
        }

factory = Factory()