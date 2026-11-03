class DecisionEngine:

    def __init__(self):

        self.MAP = {

            # MEMORY

            "memory_audit": "MemoryAgent",
            "memory_report": "MemoryAgent",

            # NETWORK

            "network_scan": "NetworkAgent",
            "network_report": "NetworkAgent",

            # HARDWARE

            "hardware_check": "HardwareAgent",
            "hardware_report": "HardwareAgent",

            # KNOWLEDGE

            "knowledge_rebuild": "KnowledgeAgent",
            "knowledge_report": "KnowledgeAgent",

            # REGISTRY

            "registry_update": "RegistryAgent",
            "passport_refresh": "RegistryAgent",

            # SERVICES

            "service_check": "ServiceAgent",
            "service_report": "ServiceAgent",

            # NODE

            "node_sync": "SyncAgent",

            "memory_report": "MemoryAgent",
            "network_report": "NetworkAgent",
            "hardware_report": "HardwareAgent",
            "service_report": "ServiceAgent",

    return self.MAP.get(task, "UnknownAgent")

         