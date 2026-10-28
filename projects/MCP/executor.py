import requests

from decision_engine import decision_engine
from task_queue import task_queue


class Executor:

    def execute(self):

        task = task_queue.dequeue()

        if not task:
            return {
                "status": "idle"
            }

        agent = decision_engine.select(task)

        #
        # TASK REMOTO
        #

        if agent == "KnowledgeAgent":

            try:

                print(f"[REMOTE] {task}")
                print("[NODE56] worker execute")

                response = requests.post(
                    "http://192.168.1.56:8000/worker/execute",
                    json={"task": task},
                    timeout=30
                )

                worker_result = response.json()

                return {
                    "task": task,
                    "agent": agent,
                    "node": "node56",
                    "status": worker_result.get(
                        "status",
                        "completed"
                    ),
                    "worker_response": worker_result
                }

            except Exception as e:

                # NON perdere il task
                task_queue.enqueue(task)

                return {
                    "task": task,
                    "agent": agent,
                    "node": "node56",
                    "status": "retry",
                    "error": str(e)
                }

        #
        # TASK LOCALI
        #

        return {
            "task": task,
            "agent": agent,
            "node": "node41",
            "status": "executed"
        }


executor = Executor()