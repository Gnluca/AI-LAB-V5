import json
import os
import requests
from framework.resource_manager import resource_manager
from framework.model_selector import model_selector

def _fallback(context):
    text = " ".join((context or {}).get("problems", [])).lower()
    goals = []
    if "node56" in text: goals.append({"goal": "Monitor Node56", "priority": 9})
    if "ram" in text or "memoria" in text: goals.append({"goal": "Analizza Memoria", "priority": 8})
    if "rete" in text or "network" in text: goals.append({"goal": "Analizza Rete", "priority": 7})
    if "ollama" in text or "servizi" in text: goals.append({"goal": "Verifica Servizi", "priority": 8})
    if not goals: goals.append({"goal": "Audit Laboratorio", "priority": 5})
    return json.dumps({"goals": goals}, ensure_ascii=False)

def reason(context, resources=None, session=None):
    resources = resources if resources is not None else resource_manager.collect()
    model = model_selector.select(resources)
    if not model: return _fallback(context)
    endpoint = os.getenv("AI_LAB_OLLAMA_GENERATE_URL", "http://127.0.0.1:11434/api/generate")
    prompt = ('Sei il Cognitive Core AI-LAB. Analizza il contesto e rispondi SOLO JSON nel formato '
              '{"goals":[{"goal":"Audit Laboratorio","priority":5}]}. Goal consentiti: '
              'Audit Laboratorio, Analizza Memoria, Analizza Rete, Controllo Hardware, Monitor Node56, '
              'Verifica Servizi, Aggiorna Registry, Sincronizza Node56, Aggiorna Knowledge Base, '
              'Health Check Completo. Priorità intera 1-10.\nCONTESTO:\n' +
              json.dumps(context or {}, ensure_ascii=False, indent=2))
    http = session or requests
    try:
        response = http.post(endpoint, json={"model": model, "prompt": prompt, "stream": False},
                             timeout=float(os.getenv("AI_LAB_OLLAMA_TIMEOUT", "45")))
        response.raise_for_status()
        data = response.json()
        answer = data.get("response") if isinstance(data, dict) else None
        return answer if isinstance(answer, str) and answer.strip() else _fallback(context)
    except (requests.RequestException, ValueError, TypeError):
        return _fallback(context)
