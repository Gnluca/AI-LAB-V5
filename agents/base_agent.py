class BaseAgent:

    def __init__(self, name):

        self.name = name

    def run(self):
        pass

    def health(self):

        return {
            "status": "healthy"
        }

    def report(self):

        return {
            "agent": self.name
        }