from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import os
import json
import requests
import sys
import json
from pathlib import Path
import psutil

mcp_path = r"E:\AI-Server\projects\MCPServer"
REGISTRY_DIR = Path(r"E:\AI-Server\registry")
PASSPORT_DIR = Path(r"E:\AI-Server\passport")
FINGERPRINT_DIR = Path(r"E:\AI-Server\fingerprint")


if mcp_path not in sys.path:
    sys.path.append(mcp_path)

from mcp_server import MCPServer

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

app = FastAPI(title="AI LAB V6.2")

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    
@app.get("/status")
def status():
    return {
        "status": "online",
        "ollama": "online",
        "model": "llama3.1",
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("C:\\").percent
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

# ------------------------------------------------------------------
# STATUS
# ------------------------------------------------------------------

@app.get("/status")
def status():

    ollama_status = "offline"
    model_name = "unknown"

    try:
        response = requests.get(
            "http://127.0.0.1:11434/api/tags",
            timeout=3
        )

        if response.status_code == 200:
            ollama_status = "online"

            models = response.json().get("models", [])

            if models:
                model_name = models[0].get("name", "unknown")

    except Exception:
        pass

    return {
        "status": "online",
        "ollama": ollama_status,
        "model": model_name
    }


# ------------------------------------------------------------------
# HARDWARE STATUS
# ------------------------------------------------------------------

@app.get("/hardware/status")
def hardware_status():

    return {
        "cpu": round(psutil.cpu_percent(interval=1), 1),
        "ram": round(psutil.virtual_memory().percent, 1),
        "disk": round(
            psutil.disk_usage("C:\\").percent,
            1
        )
    }


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
        "status": "ok"
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

@app.get("/network/lab")
def network_lab():

    result = {
        "node_41": {
            "ip": "192.168.1.41",
            "status": "online",
            "role": "primary"
        }
    }

    try:
        node56 = requests.get(
            "http://192.168.1.56:8000/status",
            timeout=5
        ).json()

        result["node_56"] = node56

    except Exception as e:

        result["node_56"] = {
            "status": "offline",
            "error": str(e)
        }

    return result

@app.get("/network/nodes")
def network_nodes():

    with open(
        r"E:\AI-Server\data\nodes.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

@app.get("/network/scan")
def network_scan():

    with open(
        r"E:\AI-Server\data\nodes.json",
        "r",
        encoding="utf-8"
    ) as f:
        registry = json.load(f)

    results = []

    for node in registry["nodes"]:

        if not node.get("enabled", True):
            continue

        try:

            if node["ip"] == "192.168.1.41":

                results.append({
                    "name": node["name"],
                    "ip": node["ip"],
                    "role": node["role"],
                    "status": {
                        "status": "online",
                        "ollama": "online",
                        "model": "llama3.1"
                    }
                })

                continue

            response = requests.get(
                f"http://{node['ip']}:8000/status",
                timeout=10
            )

            results.append({
                "name": node["name"],
                "ip": node["ip"],
                "role": node["role"],
                "status": response.json()
            })

        except Exception as e:

            results.append({
                "name": node["name"],
                "ip": node["ip"],
                "role": node["role"],
                "status": "offline",
                "error": str(e)
            })

    online_nodes = sum(
        1
        for node in results
        if isinstance(node["status"], dict)
    )

    return {
        "administrator": registry["administrator"],
        "connected_nodes": len(results),
        "online_nodes": online_nodes,
        "results": results
    }

    return {
        "administrator": registry["administrator"],
        "connected_nodes": len(results),
        "results": results
    }
# =====================================
# NETWORK AGENT
# =====================================



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

@app.get("/agent/development/status")
def development_status():
    return {
        "agent": "DevelopmentAgent",
        "status": "online"
    }

@app.get("/agent/development/audit")
def development_audit():

    import sys

    agent_path = r"E:\AI-Server\projects\DevelopmentAgent"

    if agent_path not in sys.path:
        sys.path.append(agent_path)

    from development_agent import DevelopmentAgent

    agent = DevelopmentAgent()

    return agent.audit()

@app.get("/agent/network/status")
def network_status():

    from network_agent import NetworkAgent

    agent = NetworkAgent()

    return agent.status()
    
@app.get("/agent/hardware/status")
def hardware_status():

    import sys

    agent_path = (
        r"E:\AI-Server\projects\HardwareAgent"
    )

    if agent_path not in sys.path:
        sys.path.append(agent_path)

    from hardware_agent import HardwareAgent

    agent = HardwareAgent()

    return agent.status()

   



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
    
# ============================================
# MCP SERVER
# ============================================

@app.get("/mcp/tools")
def mcp_tools():

    mcp = MCPServer()

    return mcp.list_tools()


@app.get("/mcp/call/{tool_name}")
def mcp_call(tool_name: str):

    mcp = MCPServer()

    return mcp.call_tool(tool_name)
    
    
@app.get("/registry/nodes")
def registry_nodes():

    file_path = REGISTRY_DIR / "nodes_registry.json"

    if not file_path.exists():
        return {
            "status": "error",
            "message": "nodes_registry.json not found"
        }

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/registry/resources")
def registry_resources():

    file_path = REGISTRY_DIR / "resources_registry.json"

    if not file_path.exists():
        return {
            "status": "error",
            "message": "resources_registry.json not found"
        }

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/registry/governance")
def registry_governance():

    file_path = REGISTRY_DIR / "governance_registry.json"

    if not file_path.exists():
        return {
            "status": "error",
            "message": "governance_registry.json not found"
        }

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
        
@app.get("/registry/passports")
def registry_passports():

    file_path = REGISTRY_DIR / "passports_registry.json"

    if not file_path.exists():
        return {
            "status": "error",
            "message": "passports_registry.json not found"
        }

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/registry/node41")
def node41_fingerprint():

    file_path = REGISTRY_DIR / "node41_fingerprint.json"

    if not file_path.exists():
        return {
            "status": "error",
            "message": "node41_fingerprint.json not found"
        }

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/registry/node56")
def node56_fingerprint():

    file_path = REGISTRY_DIR / "node56_fingerprint.json"

    if not file_path.exists():
        return {
            "status": "error",
            "message": "node56_fingerprint.json not found"
        }

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/registry/overview")
def registry_overview():

    return {
        "lab": "AI-LAB",
        "version": "V6.2",
        "primary_node": "node41",
        "nodes_registered": 2,
        "resources_registered": 9,
        "governance": "enabled",
        "passport_authority": "enabled"
    }

# ------------------------------------------------------------------
# REGISTRY
# ------------------------------------------------------------------

@app.get("/registry")
def registry():

    return {
        "node_id": "NODE41",
        "name": "Primary Node",
        "ip": "192.168.1.41",
        "role": "MASTER"
    }
    
# ------------------------------------------------------------------
# FINGERPRINT
# ------------------------------------------------------------------

@app.get("/fingerprint")
def fingerprint():

    return {
        "hostname": "NODE41",
        "cpu_count": psutil.cpu_count(),
        "memory_gb": round(
            psutil.virtual_memory().total / 1024**3,
            2
        )
    }
    
# ------------------------------------------------------------------
# PASSPORT
# ------------------------------------------------------------------

@app.get("/passport")
def passport():

    return {
        "node": "NODE41",
        "owner": "AI-LAB",
        "governance": "V6.2",
        "status": "ACTIVE"
    }

    
    

    