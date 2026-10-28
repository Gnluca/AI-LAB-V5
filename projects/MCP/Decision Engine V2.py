class DecisionEngine:

    TASK_ROUTING = {

        "memory_audit": {
            "agent": "MemoryAgent",
            "node": "node41"
        },

        "network_scan": {
            "agent": "NetworkAgent",
            "node": "node41"
        },

        "hardware_check": {
            "agent": "HardwareAgent",
            "node": "node41"
        },

        "knowledge_rebuild": {
            "agent": "KnowledgeAgent",
            "node": "node56"
        },

        "llm_inference": {
            "agent": "OllamaAgent",
            "node": "node56"
        }
    }

    def select(self, task):
        return self.TASK_ROUTING.get(task)

decision_engine = DecisionEngine()