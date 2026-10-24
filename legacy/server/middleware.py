from memory import search_memory


def build_context(text):

    memories = search_memory(text)

    core = []

    core += search_memory("SERVER_IP")
    core += search_memory("AI_SERVER")
    core += search_memory("GPU_SERVER")
    core += search_memory("OLLAMA_MODEL")
    core += search_memory("DATABASE")

    all_memories = core + memories

    seen = set()
    context = ""

    for item in all_memories[:3]:

        if item["id"] in seen:
            continue

        seen.add(item["id"])

        context += f"""

RICORDO #{item['id']}

Informazione:
{item['prompt']}

"""

    return context, len(seen)


def enrich_prompt(user_text):

    context, memory_count = build_context(user_text)

    full_prompt = f"""
Sei AI LAB V2.

REGOLE OBBLIGATORIE

1. Se esiste una memoria recuperata usala.
2. Non inventare informazioni.
3. Dai priorita alla memoria.
4. Se la risposta e nella memoria, usa la memoria.

MEMORIA RECUPERATA

{context}

DOMANDA

{user_text}
"""

    return full_prompt, memory_count