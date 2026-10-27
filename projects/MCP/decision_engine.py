class DecisionEngine:

    MAP = {

        "memory_audit":
        "MemoryAgent",

        "network_scan":
        "NetworkAgent",

        "hardware_check":
        "HardwareAgent",

        "knowledge_rebuild":
        "KnowledgeAgent"
    }

    def select(self, task):

        return self.MAP.get(task)

decision_engine = DecisionEngine()