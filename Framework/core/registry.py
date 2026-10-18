class Registry:

    def __init__(self):

        self.nodes = []

        self.agents = []

    def register_node(self, node):

        self.nodes.append(node)

    def register_agent(self, agent):

        self.agents.append(agent)

    def summary(self):

        return {
            "nodes": self.nodes,
            "agents": self.agents
        }