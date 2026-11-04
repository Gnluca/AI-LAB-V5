# AI-LAB V7 patched build

Install dependencies with `python -m pip install -r requirements.txt`.
Run offline regression tests with `python -m unittest discover -s tests -v`.
Run one cognitive cycle with `python -c "from cognitive_core.cognitive_loop import run_cycle; print(run_cycle())"`.
Run the persistent Master Loop with `python -m runtime.master_loop`.

Node56 is configured through `AI_LAB_NODE56_URL` (default `http://192.168.1.56:8000`) and `AI_LAB_NODE56_WORKER_URL` (defaults to base URL plus `/worker/execute`). Remote calls have configurable timeouts and bounded retries. Set `AI_LAB_OLLAMA_GENERATE_URL`, `AI_LAB_OLLAMA_TIMEOUT`, `AI_LAB_WORKER_TIMEOUT`, `AI_LAB_WORKER_MAX_ATTEMPTS`, `AI_LAB_MAX_TASKS_PER_CYCLE`, `AI_LAB_CYCLE_INTERVAL`, and `AI_LAB_DATA_DIR` as needed.

Important: task routing is aligned, but this patch does not invent local agent implementations where adapters are absent. Local tasks are reported as `accepted`, not `executed`, until a real agent adapter is wired. Test real Node56 and Ollama connectivity separately on the deployment network.

## Componenti integrati

- **Master Loop**: ciclo persistente, arresto cooperativo, stato atomico e intervallo configurabile.
- **Cognitive Loop**: osservazione → contesto → reasoning → goal → MPC → feedback.
- **Resource Framework / Manager**: provider CPU, memoria, Ollama e Node56 isolati dagli errori reciproci.
- **Model Selector**: selezione prudente tra modelli Ollama disponibili; nessun modello inventato se il servizio non risponde.
- **Goal Generator**: allowlist, deduplicazione e priorità limitata.
- **MPC Core**: pianificazione, coda e dispatch con budget e retry limitati.
- **Node56 Worker**: servizio HTTP opzionale in `framework/node56_worker.py`; espone `/worker/health` e `/worker/execute`.

Per avviare il worker sul nodo 56: `python -m pip install -r requirements.txt` e `uvicorn framework.node56_worker:app --host 0.0.0.0 --port 8000`. Registrare gli adapter reali tramite `register_handler()`. Senza adapter, il worker risponde `unavailable` (non dichiara falsamente di aver eseguito il task). Configurare firewall e rete prima dell'esposizione.
