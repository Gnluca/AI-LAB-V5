from pathlib import Path

class DevelopmentAgent:

    def __init__(self):
        self.root = Path("E:/AI-Server")

    def audit(self):
        files = list(self.root.rglob("*.py"))

        return {
            "python_files": len(files),
            "files": [str(f) for f in files]
        }

if __name__ == "__main__":
    agent = DevelopmentAgent()

    result = agent.audit()

    print(result)