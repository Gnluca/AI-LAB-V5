
class Agent:

    def __init__(self):
        self.name = "ResearchAgent"

    def run(self):

        return {
            "agent": self.name,
            "status": "running"
        }


if __name__ == "__main__":

    agent = Agent()

    print(
        agent.run()
    )
