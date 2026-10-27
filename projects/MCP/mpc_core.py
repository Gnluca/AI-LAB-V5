from goals import goal_manager
from planner import planner
from task_queue import task_queue
from executor import executor

class MPCCore:

    def create_goal(self, goal):

        item = goal_manager.create_goal(goal)

        tasks = planner.build(goal)

        for task in tasks:
            task_queue.enqueue(task)

        return item

    def execute_next(self):

        return executor.execute()

    def status(self):

        return {
            "status": "online",
            "pending_goals":
                len(goal_manager.list_goals()),

            "queue_size":
                task_queue.size()
        }

mpc = MPCCore()