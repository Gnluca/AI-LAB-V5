try:
    from .goals import goal_manager
    from .planner import planner
    from .task_queue import task_queue
    from .executor import executor

except ImportError:

    from goals import goal_manager
    from planner import planner
    from task_queue import task_queue
    from executor import executor
class MPCCore:
    def create_goal(self, goal, priority=5):
        item = goal_manager.create_goal(goal, priority)
        tasks = planner.build(goal)
        if not tasks:
            goal_manager.complete(item["id"], "unsupported")
            item["status"], item["tasks"] = "unsupported", []
            return item
        for task in tasks: task_queue.enqueue(task)
        item["tasks"] = tasks
        return item
    def execute_next(self): return executor.execute()
    def status(self):
        goals = goal_manager.list_goals()
        return {"status": "online", "pending_goals": sum(g["status"] == "pending" for g in goals),
                "goals_total": len(goals), "queue_size": task_queue.size()}
mpc = MPCCore()
