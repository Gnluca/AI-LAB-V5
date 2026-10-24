import os
import json
from datetime import datetime

PROJECTS_ROOT = r"E:\AI-Server\projects"


def create_project(name, project_type):

    project_path = os.path.join(
        PROJECTS_ROOT,
        name
    )

    folders = [
        "backend",
        "frontend",
        "database",
        "docs",
        "logs",
        "uploads",
        "config"
    ]

    # Template specializzato NIM

    if project_type.lower() == "nim":

        folders.extend([
            "agents",
            "prompts",
            "memory",
            "models"
        ])

    os.makedirs(
        project_path,
        exist_ok=True
    )

    for folder in folders:

        os.makedirs(
            os.path.join(project_path, folder),
            exist_ok=True
        )

    info = {
        "name": name,
        "type": project_type,
        "version": "1.0",
        "created": datetime.now().isoformat()
    }

    with open(
        os.path.join(project_path, "project.json"),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            info,
            f,
            indent=4,
            ensure_ascii=False
        )

    with open(
        os.path.join(project_path, "README.md"),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f"# {name}\n\n"
            f"Tipo progetto: {project_type}\n"
        )

    # Configurazione extra NIM

    if project_type.lower() == "nim":

        nim_config = {
            "project_type": "nim",
            "model": "llama3.1",
            "memory": True,
            "middleware": True,
            "agents": True,
            "version": "1.0"
        }

        with open(
            os.path.join(project_path, "nim.json"),
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                nim_config,
                f,
                indent=4,
                ensure_ascii=False
            )

    return info