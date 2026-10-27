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

        return {
            "task": task,
            "agent": agent,
            "status": "executed"
        }

executor = Executor()