import json

ALLOWED_GOALS = {
    "Audit Laboratorio", "Analizza Memoria", "Analizza Rete", "Controllo Hardware",
    "Monitor Node56", "Verifica Servizi", "Aggiorna Registry", "Sincronizza Node56",
    "Aggiorna Knowledge Base", "Health Check Completo",
}

class GoalGenerator:
    def parse(self, response_text):
        try:
            data = response_text if isinstance(response_text, dict) else json.loads(response_text or "")
        except (TypeError, json.JSONDecodeError):
            return self.fallback(str(response_text or ""))
        raw = data.get("goals", []) if isinstance(data, dict) else []
        if not isinstance(raw, list): return self.fallback(str(response_text or ""))
        goals, seen = [], set()
        for item in raw:
            if isinstance(item, str): name, priority = item, 5
            elif isinstance(item, dict): name, priority = item.get("goal"), item.get("priority", 5)
            else: continue
            if not isinstance(name, str): continue
            name = name.strip()
            if name not in ALLOWED_GOALS or name in seen: continue
            try: priority = max(1, min(10, int(priority)))
            except (TypeError, ValueError): priority = 5
            goals.append({"goal": name, "priority": priority, "status": "pending"})
            seen.add(name)
        return goals or self.fallback(str(response_text or ""))

    def fallback(self, text):
        text = (text or "").lower()
        mappings = [("node56", "Monitor Node56", 9), ("memoria", "Analizza Memoria", 8),
                    ("memory", "Analizza Memoria", 8), ("rete", "Analizza Rete", 7),
                    ("network", "Analizza Rete", 7), ("cpu", "Controllo Hardware", 8),
                    ("hardware", "Controllo Hardware", 8), ("ollama", "Verifica Servizi", 9),
                    ("servizi", "Verifica Servizi", 8), ("registry", "Aggiorna Registry", 6)]
        goals, seen = [], set()
        for keyword, name, priority in mappings:
            if keyword in text and name not in seen:
                goals.append({"goal": name, "priority": priority, "status": "pending"}); seen.add(name)
        return goals or [{"goal": "Audit Laboratorio", "priority": 5, "status": "pending"}]

goal_generator = GoalGenerator()
