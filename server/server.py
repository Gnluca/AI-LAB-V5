from fastapi import FastAPI
from pydantic import BaseModel

import os
import json
import requests

from bridge import (
    generate,
    server_status,
    list_models
)

from memory import (
    init_memory,
    save_memory,
    search_memory,
    list_memory
)

from memory import (
    init_memory,
    save_memory,
    search_memory,
    list_memory,
    list_knowledge
)


# =====================================
# INIT
# =====================================

init_memory()

PROJECTS_DIR = r"E:\AI-Server\projects"

os.makedirs(
    PROJECTS_DIR,
    exist_ok=True
)

app = FastAPI(
    title="AI LAB V5",
    version="5.0"
)

# =====================================
# MODELS
# =====================================

class Prompt(BaseModel):
    text: str


class FactoryRequest(BaseModel):
    name: str
    type: str


# =====================================
# HOME
# =====================================

@app.get("/")
def home():

    return {
        "status": "online",
        "service": "AI LAB V5",
        "model": "llama3.1"
    }


# =====================================
# CHAT
# =====================================

@app.post("/chat")
def chat(data: Prompt):

    result = generate(data.text)

    response = result.get(
        "response",
        "Nessuna risposta"
    )

    save_memory(
        prompt=data.text,
        response=response,
        source="AI-Server",
        category="conversation",
        tags="chat,llama3.1"
    )

    return {
        "response": response
    }


# =====================================
# STATUS
# =====================================

@app.get("/status")
def status():

    return server_status()


# =====================================
# MODELS
# =====================================

@app.get("/models")
def models():

    return list_models()


# =====================================
# HEALTH
# =====================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =====================================
# MEMORY
# =====================================

@app.get("/memory/list")
def memory_list_api():

    memories = list_memory()

    return {
        "count": len(memories),
        "results": memories
    }


@app.get("/memory/search")
def memory_search(q: str):

    results = search_memory(q)

    return {
        "count": len(results),
        "results": results
    }


@app.get("/memory/test")
def memory_test():

    save_memory(
        prompt="Ollama usa la porta 11434",
        response="Configurazione confermata",
        source="AI-Server",
        category="configurazione",
        tags="ollama,11434"
    )

    return {
        "status": "saved"
    }


# =====================================
# NETWORK LAB
# =====================================

@app.get("/network/lab")
def network_lab():

    return {
        "laboratory": "AI LAB",

        "primary_node": {
            "ip": "192.168.1.41",
            "role": "PRIMARY",
            "memory": "centralized",
            "status": "online"
        },

        "legacy_node": {
            "ip": "192.168.1.56",
            "role": "LEGACY",
            "status": "online"
        },

        "services": {
            "ollama": "11434",
            "fastapi": "8000",
            "model": "llama3.1"
        }
    }


# =====================================
# NETWORK AGENT
# =====================================

@app.get("/agent/network/status")
def network_agent_status():

    return {
        "agent": "NetworkAgent",
        "status": "active"
    }


@app.get("/agent/network/discover")
def network_discover():

    nodes = []

    network_nodes = [
        {
            "ip": "192.168.1.41",
            "role": "PRIMARY"
        },
        {
            "ip": "192.168.1.56",
            "role": "LEGACY"
        }
    ]

    for node in network_nodes:

        try:

            requests.get(
                f"http://{node['ip']}:8000/",
                timeout=2
            )

            nodes.append({
                "ip": node["ip"],
                "role": node["role"],
                "status": "online"
            })

        except Exception:

            nodes.append({
                "ip": node["ip"],
                "role": node["role"],
                "status": "offline"
            })

    return {
        "agent": "NetworkAgent",
        "nodes": nodes
    }
    
    
@app.get("/agent/labmanager/governance")
def labmanager_governance():

    with open(
        r"E:\AI-Server\ARCHITETTURA.md",
        "r",
        encoding="utf-8"
    ) as f:

        content = f.read()

    return {
        "agent": "LabManager",
        "governance": content
    }


# =====================================
# MEMORY AGENT
# ==========================

@app.get("/agent/memory/status")
def memory_agent_status():

    memories = list_memory()

    return {
        "agent": "MemoryAgent",
        "status": "active",
        "records": len(memories)
    }


@app.get("/agent/memory/summary")
def memory_summary():

    memories = list_memory()

    return {
        "agent": "MemoryAgent",
        "records": len(memories),
        "message": "Memory operational"
    }


@app.get("/agent/labmanager/status")
def labmanager_status():

    return {
        "agent": "LabManager",
        "status": "active",
        "memory_records": len(list_memory()),
        "primary_node": "192.168.1.41"
    }


@app.post("/agent/architect")
def architect_agent(data: Prompt):

    prompt = f"""
Agisci come Architect Agent.

Idea:
{data.text}

Produci:
- Obiettivo
- Componenti
- Database
- API
- Roadmap
"""

    result = generate(prompt)

    return {
        "response": result.get("response", "")
    }
    
    
# =====================================
# FACTORY
# ===================================== 

@app.post("/factory/create")
def factory_create(data: FactoryRequest):

    agent_dir = os.path.join(
        PROJECTS_DIR,
        data.name
    )

    os.makedirs(
        agent_dir,
        exist_ok=True
    )

    with open(
        os.path.join(agent_dir, "agent.json"),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump({
            "name": data.name,
            "type": data.type,
            "version": "1.0",
            "status": "created"
        }, f, indent=4)

    save_memory(
        prompt=f"Factory create {data.name}",
        response=f"Created {data.type}",
        source="Factory",
        category="factory",
        tags=f"factory,{data.type}"
    )

    return {
        "status": "created",
        "name": data.name,
        "type": data.type,
        "path": agent_dir
    }


@app.get("/factory/list")
def factory_list():

    agents = search_memory("factory")

    return {
        "count": len(agents),
        "agents": agents
    }


@app.get("/factory/status")
def factory_status():

    agents = search_memory("factory")
    memories = list_memory()

    return {
        "factory": "online",
        "agents": len(agents),
        "memory_records": len(memories),

        "primary_node": "192.168.1.41",
        "legacy_node": "192.168.1.56",

        "ollama": "online",
        "model": "llama3.1"
    }
    
@app.get("/agent/memory/snapshot")
def memory_snapshot():

    memory = list_memory()

    factory = search_memory("factory")

    return {
        "agent": "MemoryAgent",
        "memory_records": len(memory),
        "factory_records": len(factory),
        "primary_node": "192.168.1.41",
        "legacy_node": "192.168.1.56"
    }
 
@app.get("/agent/memory/build")
def memory_build():

    from database import cursor, conn

    knowledge = [

        (
            "Primary Node",
            "network",
            "192.168.1.41",
            "MemoryAgentV1",
            1.0
        ),

        (
            "Legacy Node",
            "network",
            "192.168.1.56",
            "MemoryAgentV1",
            1.0
        ),

        (
            "AI Model",
            "software",
            "llama3.1",
            "MemoryAgentV1",
            1.0
        ),

        (
            "Ollama Port",
            "configuration",
            "11434",
            "MemoryAgentV1",
            1.0
        ),

        (
            "FastAPI Port",
            "configuration",
            "8000",
            "MemoryAgentV1",
            1.0
        ),

        (
            "Primary GPU",
            "hardware",
            "RTX 4060",
            "MemoryAgentV1",
            1.0
        )

    ]

    for item in knowledge:

        cursor.execute("""
        INSERT INTO knowledge
        (
            topic,
            category,
            content,
            source,
            confidence
        )
        VALUES (?, ?, ?, ?, ?)
        """, item)

    conn.commit()

    return {
        "status": "built",
        "records": len(knowledge)
    }
    
    
# =====================================
# KNOWLEDGE BASE
# =====================================

@app.get("/knowledge/list")
def knowledge_list():

    records = list_knowledge()

    return {
        "count": len(records),
        "knowledge": records
    }
    
@app.get("/knowledge/status")
def knowledge_status():

    records = list_knowledge()

    return {
        "status": "online",
        "knowledge_records": len(records)
    }

    
@app.get("/knowledge/summary")
def knowledge_summary():

    from database import cursor

    categories = [
        "hardware",
        "software",
        "configuration",
        "network",
        "agents",
        "governance",
        "projects"
    ]

    summary = {}

    for category in categories:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM knowledge
            WHERE category = ?
            """,
            (category,)
        )

        summary[category] = cursor.fetchone()[0]

    return {
        "knowledge_records": sum(summary.values()),
        "summary": summary
    }
    
    
@app.get("/agent/memory/rebuild")
def memory_rebuild():

    from database import cursor, conn

    cursor.execute(
        "DELETE FROM knowledge"
    )

    knowledge = [

        (
            "Primary Node",
            "network",
            "192.168.1.41",
            "MemoryAgentV1",
            1.0
        ),

        (
            "Legacy Node",
            "network",
            "192.168.1.56",
            "MemoryAgentV1",
            1.0
        ),

        (
            "AI Model",
            "software",
            "llama3.1",
            "MemoryAgentV1",
            1.0
        ),

        (
            "Ollama Port",
            "configuration",
            "11434",
            "MemoryAgentV1",
            1.0
        ),

        (
            "FastAPI Port",
            "configuration",
            "8000",
            "MemoryAgentV1",
            1.0
        ),

        (
            "Primary GPU",
            "hardware",
            "RTX 4060",
            "MemoryAgentV1",
            1.0
        )

    ]

    for item in knowledge:

        cursor.execute("""
        INSERT INTO knowledge
        (
            topic,
            category,
            content,
            source,
            confidence
        )
        VALUES (?, ?, ?, ?, ?)
        """, item)

    conn.commit()

    return {
        "status": "rebuilt",
        "records": len(knowledge)
    }


@app.get("/agent/memory/audit")
def memory_audit():

    memory = list_memory()
    knowledge = list_knowledge()

    memory_records = len(memory)
    knowledge_records = len(knowledge)

    if memory_records > 0:
        coverage = round(
            (knowledge_records / memory_records) * 100,
            2
        )
    else:
        coverage = 0

    return {
        "agent": "MemoryAgent",
        "memory_records": memory_records,
        "knowledge_records": knowledge_records,
        "coverage_percent": coverage,
        "status": "building"
    }

    
@app.get("/agent/inventory/build")
def inventory_build():

    from database import cursor, conn

    cursor.execute(
        "DELETE FROM inventory"
    )

    assets = [

        (
            "server",
            "AI-Server",
            "E:\\AI-Server",
            "active"
        ),

        (
            "project",
            "MemoryAgentV1",
            "E:\\AI-Server\\projects\\MemoryAgentV1",
            "active"
        ),

        (
            "backup",
            "Backup",
            "E:\\Backup",
            "active"
        ),

        (
            "project",
            "SocialAI",
            "E:\\SocialAI",
            "active"
        ),

        (
            "project",
            "AI-Learning-Studio",
            "E:\\AI-Learning-Studio",
            "active"
        )

    ]

    for item in assets:

        cursor.execute("""
        INSERT INTO inventory
        (
            category,
            name,
            path,
            status
        )
        VALUES (?, ?, ?, ?)
        """, item)

    conn.commit()

    return {
        "status": "built",
        "records": len(assets)
    }


@app.get("/inventory/list")
def inventory_list():

    from database import cursor

    cursor.execute("""
    SELECT *
    FROM inventory
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    return {
        "count": len(rows),
        "inventory": rows
    }

    
@app.get("/agent/inventory/audit")
def inventory_audit():

    from database import cursor

    cursor.execute(
        "SELECT COUNT(*) FROM inventory"
    )

    records = cursor.fetchone()[0]

    return {
        "agent": "InventoryAgent",
        "inventory_records": records,
        "drives": [
            "C:",
            "E:",
            "F:"
        ],
        "status": "healthy"
    }

    