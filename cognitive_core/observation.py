from datetime import datetime, timezone
from framework.resource_manager import resource_manager

def build_observation():
    resources = resource_manager.collect()
    cpu = resources.get("cpu") or {"resource": "cpu", "usage": 0, "status": "unknown"}
    memory = resources.get("memory") or {"resource": "ram", "usage": 0, "status": "unknown"}
    ollama = resources.get("ollama") or {"resource": "ollama", "models": [], "status": "unknown"}
    node = resources.get("node56") or {"resource": "node56", "status": "unknown"}
    alerts = []
    if cpu.get("status") in ("warning", "critical"): alerts.append(f"CPU {cpu.get('status')}")
    try:
        if float(memory.get("usage", 0)) > 85: alerts.append("RAM usage high")
    except (TypeError, ValueError): pass
    if ollama.get("status") != "online": alerts.append("Ollama offline")
    if node.get("status") != "online": alerts.append("Node56 offline")
    return {"timestamp": datetime.now(timezone.utc).isoformat(), "node41": "online",
            "node56": node.get("status", "unknown"), "node_details": node,
            "cpu": cpu, "memory": memory, "ollama": ollama, "alerts": alerts}
