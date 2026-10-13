import os
import json

def create_agent(base_path, name, role):

    agent_name = name.lower()

    os.makedirs(
        os.path.join(base_path, "agents"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(base_path, "prompts"),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(base_path, "runtime"),
        exist_ok=True
    )

    agent = {
        "name": name,
        "role": role,
        "model": "llama3.1",
        "active": True
    }

    with open(
        os.path.join(
            base_path,
            "agents",
            f"{agent_name}.json"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            agent,
            f,
            indent=4
        )

    prompt = f"""
Sei {name}.

Ruolo:

{role}

Rispondi sempre in italiano.
"""

    with open(
        os.path.join(
            base_path,
            "prompts",
            f"{agent_name}.txt"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(prompt)

    runtime = {
        "agent": name,
        "prompt": f"{agent_name}.txt",
        "model": "llama3.1",
        "active": True
    }

    with open(
        os.path.join(
            base_path,
            "runtime",
            f"{agent_name}_runtime.json"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            runtime,
            f,
            indent=4
        )