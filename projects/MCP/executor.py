import requests

try:
    from .decision_engine import decision_engine
    from .task_queue import task_queue
except ImportError:
    from decision_engine import decision_engine
    from task_queue import task_queue

from adapters.agents.memory_adapter import memory_adapter
from adapters.agents.network_adapter import network_adapter
from adapters.agents.hardware_adapter import hardware_adapter
from adapters.agents.service_adapter import service_adapter


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
        # MEMORY
        #

        if task in [
            "memory_audit",
            "memory_report"
        ]:
            return memory_adapter.run(task)

        #
        # NETWORK
        #

        if task in [
            "network_scan",
            "network_report"
        ]:
            return network_adapter.run(task)

        #
        # HARDWARE
        #

        if task in [
            "hardware_check",
            "hardware_report"
        ]:
            return hardware_adapter.run(task)

        #
        # SERVICES
        #

        if task in [
            "service_check",
            "service_report"
        ]:
            return service_adapter.run(task)

        #
        # REMOTE TASKS
        #

        if agent == "KnowledgeAgent":

            try:

                url = "http://127.0.0.1:8000/worker/execute"

                print(f"[REMOTE] {task}")
                print(f"[URL] {url}")

                response = requests.post(
                    url,
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

                return {
                    "task": task,
                    "agent": agent,
                    "node": "node56",
                    "status": "failed",
                    "error": str(e)
                }

        #
        # DEFAULT
        #

        return {
            "task": task,
            "agent": agent,
            "node": "node41",
            "status": "accepted",
            "detail": "Recognized task; adapter not configured"
        }


executor = Executor()