import requests

try:
    from .decision_engine import decision_engine
    from .task_queue import task_queue
except ImportError:
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

        if agent == "UnknownAgent":

            return {
                "task": task,
                "agent": agent,
                "node": "node41",
                "status": "unknown_task"
            }

        #
        # TASK REMOTO
        #

        if agent == "KnowledgeAgent":

            try:

                print(f"[REMOTE] {task}")

                url = "http://127.0.0.1:8000/worker/execute"

                print(f"[REMOTE URL] {url}")

                response = requests.post(
                    url,
                    json={"task": task},
                    timeout=30
                )

                print("STATUS CODE:", response.status_code)
                print("RESPONSE:", response.text)

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