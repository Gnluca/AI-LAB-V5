from projects.MCP.decision_engine import DecisionEngine, decision_engine

if __name__ == "__main__":
    print("Known task mappings:")
    for task, agent in decision_engine.MAP.items():
        print(f"{task}: {agent}")
