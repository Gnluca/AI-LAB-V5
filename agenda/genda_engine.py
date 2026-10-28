import json
from pathlib import Path

AGENDA_FILE = Path(__file__).parent / "agenda.json"


class Agenda:

    def __init__(self):
        self.tasks = self._load()

    def _load(self):
        if AGENDA_FILE.exists():
            try:
                return json.loads(AGENDA_FILE.read_text(encoding="utf-8"))
            except:
                pass

        return [
            {
                "id": 1,
                "time": "08:00",
                "goal": "Audit Sistema",
                "status": "pending"
            },
            {
                "id": 2,
                "time": "12:00",
                "goal": "Verifica Node56",
                "status": "pending"
            },
            {
                "id": 3,
                "time": "18:00",
                "goal": "Aggiorna Knowledge",
                "status": "pending"
            }
        ]

    def save(self):
        AGENDA_FILE.write_text(
            json.dumps(self.tasks, indent=2),
            encoding="utf-8"
        )

    def get_tasks(self):
        return self.tasks

    def run(self):
        return self.tasks


agenda = Agenda()