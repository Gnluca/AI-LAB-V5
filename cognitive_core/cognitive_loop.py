import json
import sys

from pathlib import Path
from datetime import datetime
from goal_generator import goal_generator

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

#
# Import compatibili sia come script sia come package
#

try:
    from .observation import build_observation
    from .context_builder import build_context
    from .reasoning_engine import reason
except ImportError:
    from observation import build_observation
    from context_builder import build_context
    from reasoning_engine import reason
    from goal_generator import goal_generator

try:
    from projects.MCP.mpc_core import mpc
except Exception as e:
    print(f"[ERROR] MPC Core non disponibile: {e}")
    mpc = None

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

REPORT_FILE = DATA_DIR / "cognitive_report.json"
FEEDBACK_FILE = DATA_DIR / "feedback.json"


def extract_goals(reasoning_text):

    goals = []

    if not reasoning_text:
        return ["Audit Laboratorio"]

    text = reasoning_text.lower()

    if "node56" in text:
        goals.append("Monitor Node56")

    if "registry" in text:
        goals.append("Aggiorna Registry")

    if "servizi" in text or "service" in text:
        goals.append("Verifica Servizi")

    if "rete" in text or "network" in text:
        goals.append("Analizza Rete")

    if "hardware" in text:
        goals.append("Controllo Hardware")

    if "memoria" in text:
        goals.append("Analizza Memoria")

    if not goals:
        goals.append("Audit Laboratorio")

    return list(set(goals))


def save_report(
    observation,
    context,
    reasoning,
    goals
):

    report = {
        "timestamp": datetime.now().isoformat(),
        "observation": observation,
        "context": context,
        "reasoning": reasoning,
        "goals": goals
    }

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
        )


def save_feedback(results):

    feedback = []

    if FEEDBACK_FILE.exists():

        try:

            with open(
                FEEDBACK_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                feedback = json.load(f)

        except Exception:
            feedback = []

    feedback.append(
        {
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
    )

    with open(
        FEEDBACK_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            feedback,
            f,
            indent=4,
            ensure_ascii=False
        )


def execute_tasks():

    if not mpc:
        return []

    results = []

    while True:

        status = mpc.status()

        if status["queue_size"] == 0:
            break

        result = mpc.execute_next()

        results.append(result)

        print(result)

    return results


def run_cycle():

    print()
    print("===================================")
    print("AI-LAB COGNITIVE CYCLE")
    print("===================================")

    #
    # OSSERVAZIONE
    #

    observation = build_observation()

    print()
    print("[OBSERVATION]")
    print(observation)

    #
    # CONTESTO
    #

    context = build_context(
        observation
    )

    print()
    print("[CONTEXT]")
    print(context)

    #
    # RAGIONAMENTO
    #

    reasoning = reason(
        context
    )

    print()
    print("[REASONING]")
    print(reasoning)

    #
    # GOAL
    #

    goals = goal_generator.parse(
    reasoning
   )

    print()
    print("[GOALS]")
    print(goals)

    save_report(
        observation,
        context,
        reasoning,
        goals
    )

    if not mpc:

        return {
            "status": "warning",
            "message": "MPC non disponibile"
        }

    created_goals = []

    # rimuove duplicati

    unique = {}

    for goal in goals:
        unique[goal["goal"]] = goal

    goals = list(unique.values())

    # ordina per priorità
    goals.sort(
        key=lambda x: x["priority"],
        reverse=True
    )

    for goal_data in goals:
        item = mpc.create_goal(goal_data["goal"])
        created_goals.append(item)

        print(
            f"[GOAL] {goal_data['goal']} "
            f"(priority={goal_data['priority']})"
        )

    print()
    print("[MPC STATUS]")
    print(mpc.status())

    print()
    print("[TASK EXECUTION]")

    results = execute_tasks()

    save_feedback(results)

    print()
    print("[FINAL STATUS]")
    print(mpc.status())

    return {
        "status": "success",
        "goals": created_goals,
        "executed_tasks": len(results)
    }


if __name__ == "__main__":

    result = run_cycle()

    print()
    print("[RESULT]")
    print(result)