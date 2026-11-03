import json
import requests
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from framework.resource_manager import resource_manager
from framework.model_selector import model_selector

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

resources = resource_manager.collect()

MODEL = model_selector.select(
    resources
)

print(f"[MODEL] {MODEL}")

def extract_goals(response_text):

    goals = []

    text = response_text.lower()

    if "obiettiv" in text:

        if "monitoraggio" in text:
            goals.append("Audit Laboratorio")

        if "analizzare" in text:
            goals.append("Audit Laboratorio")

        if "network" in text:
            goals.append("Audit Laboratorio")

    if not goals:
        goals.append("Audit Laboratorio")

    return goals 

def reason(context):

    prompt = f"""
Sei il Cognitive Core di AI-LAB.

Analizza il contesto.

CONTESTO:

{json.dumps(context, indent=2)}

Rispondi SOLO in JSON.

Formato:

{{
  "goals": [
    {{
      "goal": "Monitor Node56",
      "priority": 10
    }}
  ]
}}

Formato consentito:

{
  "goals": [
    {
      "goal": "<goal esistente>",
      "priority": 1-10
    }
  ]
}

Goal consentiti:

- Audit Laboratorio
- Analizza Memoria
- Analizza Rete
- Controllo Hardware
- Monitor Node56
- Verifica Servizi
- Aggiorna Registry

Non aggiungere spiegazioni.
"""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300
        )

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            print(response.text)
            return None

        data = response.json()

        return data.get("response", "")

    except Exception as e:
        print("ERRORE:", e)
        return None


if __name__ == "__main__":

    test_context = {
        "status": "attention",
        "problems": [
            "nessun obiettivo attivo"
        ]
    }

    result = reason(test_context)

    print("\n=== RISPOSTA OLLAMA ===\n")

    print(result)