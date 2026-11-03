import json
import re


class GoalGenerator:

    def parse(self, response_text):

        if not response_text:
            return [
                {
                    "goal": "Audit Laboratorio",
                    "priority": 5,
                    "status": "pending"
                }
            ]

        try:

            data = json.loads(response_text)

            goals = data.get("goals", [])

            normalized = []

            for goal in goals:

                normalized.append(
                    {
                        "goal": goal.get("goal"),
                        "priority": goal.get(
                            "priority",
                            5
                        ),
                        "status": "pending"
                    }
                )

            return normalized

        except Exception:

            return self.fallback(
                response_text
            )

    def fallback(self, text):

        goals = []

        if not text:
            return [
                {
                    "goal": "Audit Laboratorio",
                    "priority": 5,
                    "status": "pending"
                }
            ]

        text = text.lower()

        mappings = {

            "memoria": (
                "Analizza Memoria",
                8
            ),

            "network": (
                "Analizza Rete",
                7
            ),

            "rete": (
                "Analizza Rete",
                7
            ),

            "node56": (
                "Monitor Node56",
                9
            ),

            "ollama": (
                "Verifica Servizi",
                9
            ),

            "cpu": (
                "Controllo Hardware",
                8
            ),

            "hardware": (
                "Controllo Hardware",
                8
            )
        }

        for keyword, value in mappings.items():

            if keyword in text:

                goals.append(
                    {
                        "goal": value[0],
                        "priority": value[1],
                        "status": "pending"
                    }
                )

        if not goals:

            goals.append(
                {
                    "goal": "Audit Laboratorio",
                    "priority": 5,
                    "status": "pending"
                }
            )

        return goals


goal_generator = GoalGenerator()


if __name__ == "__main__":

    sample = """
    {
        "goals": [
            {
                "goal": "Monitor Node56",
                "priority": 10
            },
            {
                "goal": "Analizza Memoria",
                "priority": 8
            }
        ]
    }
    """

    print(
        goal_generator.parse(sample)
    )