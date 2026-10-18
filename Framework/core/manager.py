class LabManager:

    def __init__(self):

        self.version = "6.2"

        self.status = "running"

        self.agents = []

        self.nodes = []

    def register_agent(self, name):

        self.agents.append(name)

    def register_node(self, ip):

        self.nodes.append(ip)

    def get_status(self):

        return {
            "version": self.version,
            "status": self.status,
            "agents": len(self.agents),
            "nodes": len(self.nodes)
        }