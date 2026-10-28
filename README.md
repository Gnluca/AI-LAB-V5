# AI LAB

Runtime FastAPI per il laboratorio AI, con agenti opzionali, monitor hardware e integrazione Ollama.

## Stato della versione

Questa revisione punta alla stabilità: avvio multipiattaforma, percorsi relativi al progetto, timeout sulle chiamate di rete, health check espliciti e funzionamento in modalità **degraded** quando Ollama, psutil o un nodo remoto non sono disponibili.

## Installazione

```bash
python3 -m venv .venv
. .venv/bin/activate              # Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
```

## Avvio API

```bash
python -m uvicorn server.app:app --host 0.0.0.0 --port 8000
```

Variabili supportate: `AI_LAB_HOST`, `AI_LAB_PORT`, `AI_LAB_VERSION`, `AI_LAB_CORS_ORIGINS`, `OLLAMA_URL`, `OLLAMA_MODEL` e `OLLAMA_TIMEOUT`.

## Verifica

```bash
python3 -m py_compile $(find . -name '*.py')
python3 test_stability.py
python3 test_node56.py
```

Il test del nodo 56 restituisce un risultato `reachable: false` se il nodo non è raggiungibile, senza far fallire l’intero progetto. Per cambiare endpoint: `AI_LAB_NODE56_URL=http://host:8000/status python3 test_node56.py`.

## Endpoint principali

- `GET /` — informazioni del servizio
- `GET /status` — stato API e Ollama
- `GET /health` — salute del processo API e dipendenze
- `GET /hardware` — metriche hardware, se disponibili

Ollama è una dipendenza opzionale: l’API resta avviabile anche quando il servizio modello è offline.
