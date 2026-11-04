class Planner:
    TEMPLATES = {
        "Audit Laboratorio": ["memory_audit", "network_scan", "hardware_check", "knowledge_rebuild"],
        "Monitor Node56": ["hardware_check", "network_scan", "service_check"],
        "Aggiorna Registry": ["registry_update", "passport_refresh"],
        "Verifica Servizi": ["service_check", "service_report"],
        "Analizza Memoria": ["memory_audit", "memory_report"],
        "Analizza Rete": ["network_scan", "network_report"],
        "Controllo Hardware": ["hardware_check", "hardware_report"],
        "Sincronizza Node56": ["node_sync", "registry_update"],
        "Aggiorna Knowledge Base": ["knowledge_rebuild", "knowledge_report"],
        "Health Check Completo": ["hardware_check", "network_scan", "memory_audit", "service_check"],
    }
    def build(self, goal): return list(self.TEMPLATES.get(goal, []))
planner = Planner()
