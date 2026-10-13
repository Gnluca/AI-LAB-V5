AI LAB V5

========================================
PRIMARY NODE
========================================

IP:
192.168.1.41

Role:
PRIMARY

Services:
FastAPI  : 8000
Ollama   : 11434
Model    : llama3.1
Database : chat.db

GPU:
RTX 4060

========================================
LEGACY NODE
========================================

IP:
192.168.1.56

Role:
LEGACY

Services:
/
/chat
/history

========================================
MEMORY
========================================

Database:
E:\AI-Server\database\chat.db

Endpoints:

/memory/search
/memory/list
/memory/test

Records:
Centralized

========================================
NETWORK
========================================

Endpoint:
/network/lab

Topology:

PRIMARY
192.168.1.41

LEGACY
192.168.1.56

========================================
FACTORY
========================================

Endpoints:

/factory/create
/factory/list
/factory/status

Projects:

E:\AI-Server\projects

========================================
AGENTS
========================================

MemoryAgent
NetworkAgent
LabManager
ArchitectAgent
ResearchAgent

========================================
RULES
========================================

## ========================================
REGOLA 11 - NODE ISOLATION

PRIMARY NODE
192.168.1.41

Authority:
FULL

Known Components:

- Ollama
- FastAPI
- Factory
- Memory
- Network
- Agents
- Database
- Governance

---------------------------------

LEGACY NODE
192.168.1.56

Authority:
LIMITED

Known Components:

- Chat
- History

Restricted Knowledge:

- Factory
- Memory Centralized
- Agent Registry
- Network Topology
- Governance Rules
- Internal Architecture
- Database Structure
- Ollama Configuration

---------------------------------

CLIENT NODES

Known Components:

- Public API only

Accessible Endpoints:

/
/chat
/status
/models
/network/lab
/factory/status

Forbidden Knowledge:

- Internal Architecture
- Agent Structure
- Memory Database
- Factory Operations
- Private Endpoints

---------------------------------

LAB POLICY

All requests must pass through:

192.168.1.41

No secondary node may become
the source of truth.

The primary node is the only
authority for:

- Memory
- Routing
- Factory
- Governance
- Knowledge

---------------------------------

VERIFICATION

2026-10-10

Node 192.168.1.56 was tested.

Results:

- Unable to describe node 192.168.1.41
- Unable to identify AI LAB
- Unable to identify registered agents

Isolation Status:

SUCCESS

REGOLA 12 - KNOWLEDGE OWNERSHIP

Primary Node owns:
- Memory
- Factory
- Governance
- Agent Registry
- Network Topology

Secondary Nodes own:
- Local execution
- Local history

No secondary node may become
a source of truth.


1. Memory is centralized on 192.168.1.41

2. Clients never connect directly to Ollama

3. Clients only use:
   http://192.168.1.41:8000

4. LabManager controls routing

5. Factory manages agent creation

6. All knowledge is stored in chat.db

========================================
STATUS
========================================

AI LAB V5
ACTIVE

## GOVERNANCE

PRIMARY NODE
192.168.1.41

Authority:
FULL

Responsibilities:
- Memory
- Factory
- Routing
- Agents
- Knowledge

---------------------------------

LEGACY NODE
192.168.1.56

Authority:
LIMITED

Responsibilities:
- Chat
- History

Restrictions:
- Cannot manage Factory
- Cannot manage Memory
- Cannot modify Rules

---------------------------------

CLIENT NODES

Responsibilities:
- Use public APIs only

Restrictions:
- Cannot access Ollama directly
- Cannot access database directly
- Cannot access private endpoints

---------------------------------

PUBLIC API

/
/chat
/status
/models
/network/lab
/factory/status

---------------------------------

PRIVATE API

/memory/list
/memory/search
/factory/create
/factory/list

---------------------------------

LAB POLICY

1. Memory First
2. Centralized Knowledge
3. Single Source of Truth
4. Primary Node Controls Routing
5. Factory Creates Agents
6. Agents Must Be Registered

## ========================================
GOLDEN RULES

REGOLA D'ORO 1
SINGLE SOURCE OF TRUTH

La memoria ufficiale esiste solo sul nodo:

192.168.1.41

Nessun altro nodo può diventare
fonte ufficiale della conoscenza.

---------------------------------

REGOLA D'ORO 2
MEMORY FIRST

Prima di interrogare il modello:

Utente
↓
Memoria
↓
Contesto
↓
LLM
↓
Risposta

Mai il contrario.

---------------------------------

REGOLA D'ORO 3
PRIMARY CONTROLS ROUTING

Ogni richiesta deve passare da:

192.168.1.41

I client non scelgono i nodi.

Il LabManager decide.

---------------------------------

REGOLA D'ORO 4
CLIENTS SEE ONLY THE GATEWAY

I client conoscono solo:

192.168.1.41:8000

I client non devono conoscere:

- Ollama
- Memory
- Database
- Factory
- Agenti interni
- Struttura del laboratorio

---------------------------------

REGOLA D'ORO 5
NO AGENT WITHOUT REGISTRATION

Ogni agente deve:

1. Essere creato dalla Factory
2. Essere registrato
3. Comparire in /factory/list
4. Comparire in /factory/status

---------------------------------

REGOLA D'ORO 6
KNOWLEDGE BEFORE EXECUTION

Prima di creare:

- Progetti
- Agenti
- Decisioni

il sistema deve consultare:

- Memoria
- Governance
- Conoscenza esistente

---------------------------------

REGOLA D'ORO 7
GOVERNANCE IS LAW

Le regole contenute in:

ARCHITETTURA.md

sono la fonte ufficiale
di comportamento del laboratorio.

LabManager deve rispettarle.

---------------------------------

REGOLA D'ORO 8
ISOLATION OF SECONDARY NODES

I nodi secondari:

- non conoscono la topologia completa
- non conoscono la governance
- non conoscono il registry completo
- non conoscono l'architettura interna

Verificato il:

2026-10-10

Status:

SUCCESS

---------------------------------

REGOLA D'ORO 9
EVERYTHING IS OBSERVABLE

Ogni componente deve avere:

- status
- logica verificabile
- endpoint di controllo

Nessun componente deve
operare in modo invisibile.

---------------------------------

REGOLA D'ORO 10
AI LAB BEFORE AI MODEL

Il laboratorio è più importante
del singolo modello.

I modelli possono cambiare.

La memoria, le regole,
la conoscenza e la governance
devono sopravvivere.

REGOLA D'ORO 11

EXECUTION WITHOUT KNOWLEDGE

I nodi secondari possono:

- eseguire task
- generare contenuti
- elaborare richieste

I nodi secondari non possono:

- conoscere la governance
- conoscere la topologia completa
- conoscere il registry agenti
- conoscere la memoria centrale

Il lavoro viene assegnato dal nodo primario.