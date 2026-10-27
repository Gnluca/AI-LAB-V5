class Scheduler:

    def status(self):

        return {
            "jobs": [
                "network_scan",
                "memory_audit",
                "knowledge_rebuild"
            ]
        }

scheduler = Scheduler()