import json
import sys

from pathlib import Path
from datetime import datetime

#
# PATH
#

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

#
# IMPORTS
#

try:
    from .observation import build_observation
    from .context_builder import build_context
    from .reasoning_engine import reason
    from .goal_generator import goal_generator

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

#
# FILES
#

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

REPORT_FILE = DATA_DIR / "cognitive_report.json"
FEEDBACK_FILE = DATA_DIR / "feedback.json"

#
# REPORT
#

def save_report(
    observation,
    context,
    reasoning,
    goals
):

    report = {
        "timestamp": datetime.utcnow().isoformat(),
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
            indent=2,
            ensure_ascii=False
        )


#
# FEEDBACK
#

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
            "timestamp": datetime.utcnow().isoformat(),
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
            indent=2,
            ensure_ascii=False
        )


#
# EXECUTION
#

def execute_tasks():

    if not mpc:

        return []

    results = []

    safety_counter = 0
    max_tasks = 50

    while True:

        status = mpc.status()

        if status["queue_size"] == 0:
            break

        result = mpc.execute_next()

        results.append(result)

        print(result)

        safety_counter += 1

        if safety_counter >= max_tasks:

            print(
                "[WARNING] task budget reached"
            )
            break

    return results


#
# CYCLE
#

def run_cycle():

    print()
    print("===================================")
    print("AI-LAB COGNITIVE CYCLE")
    print("===================================")

    #
    # OBSERVATION
    #

    observation = build_observation()

    print()
    print("[OBSERVATION]")
    print(observation)

    #
    # CONTEXT
    #

    context = build_context(
        observation
    )

    print()
    print("[CONTEXT]")
    print(context)

    #
    # REASONING
    #

    reasoning = reason(
        context
    )

    print()
    print("[REASONING]")
    print(reasoning)

    #
    # GOALS
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

    #
    # MPC
    #

    created_goals = []
