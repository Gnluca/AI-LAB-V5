def discover_network():

    return {
        "agent": "NetworkAgent",
        "status": "online",
        "nodes": [
            {
                "name": "Node41",
                "ip": "192.168.1.41",
                "status": "ONLINE"
            },
            {
                "name": "Node56",
                "ip": "192.168.1.56",
                "status": "ONLINE"
            }
        ],
        "services": [
            "FastAPI",
            "Ollama",
            "Dashboard"
        ],
        "active_agents": [
            "LabManager",
            "MemoryAgent",
            "InventoryAgent",
            "KnowledgeAgent",
            "HardwareAgent"
        ]
    }