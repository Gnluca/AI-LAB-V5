def build_context(observation):
    observation = observation or {}
    context = {"status": "healthy", "problems": [], "recommendations": []}
    def number(section, key):
        try: return float((observation.get(section) or {}).get(key, 0))
        except (TypeError, ValueError): return 0.0
    cpu, ram = number("cpu", "usage"), number("memory", "usage")
    if cpu > 85: context["status"] = "warning"; context["problems"].append(f"CPU elevata ({cpu:g}%)")
    if ram > 85: context["status"] = "warning"; context["problems"].append(f"RAM elevata ({ram:g}%)")
    if (observation.get("ollama") or {}).get("status") != "online":
        context["status"] = "critical"; context["problems"].append("Ollama offline")
    if observation.get("node56") != "online":
        if context["status"] == "healthy": context["status"] = "warning"
        context["problems"].append("Node56 offline")
    if not context["problems"]: context["recommendations"].append("Sistema stabile")
    return context
