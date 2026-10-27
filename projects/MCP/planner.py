class Planner:

    def build(self, goal):

        templates = {

            "Audit Laboratorio": [
                "memory_audit",
                "network_scan",
                "hardware_check",
                "knowledge_rebuild"
            ]
        }

        return templates.get(
            goal,
            ["memory_audit"]
        )

planner = Planner()