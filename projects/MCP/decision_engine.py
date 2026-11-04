class DecisionEngine:
    MAP = {
        "memory_audit": "MemoryAgent", "memory_report": "MemoryAgent",
        "network_scan": "NetworkAgent", "network_report": "NetworkAgent",
        "hardware_check": "HardwareAgent", "hardware_report": "HardwareAgent",
        "knowledge_rebuild": "KnowledgeAgent", "knowledge_report": "KnowledgeAgent",
        "registry_update": "RegistryAgent", "passport_refresh": "RegistryAgent",
        "service_check": "ServiceAgent", "service_report": "ServiceAgent",
        "node_sync": "SyncAgent",
    }
    def select(self, task): return self.MAP.get(task)

decision_engine = DecisionEngine()
