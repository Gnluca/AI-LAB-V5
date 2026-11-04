from threading import RLock
class GoalManager:
    def __init__(self): self.goals, self._lock = [], RLock()
    def create_goal(self, goal, priority=5):
        if not isinstance(goal, str) or not goal.strip(): raise ValueError("goal must be non-empty")
        with self._lock:
            item = {"id": (self.goals[-1]["id"] + 1) if self.goals else 1,
                    "goal": goal.strip(), "priority": max(1, min(10, int(priority))), "status": "pending"}
            self.goals.append(item); return dict(item)
    def list_goals(self):
        with self._lock: return [dict(g) for g in self.goals]
    def complete(self, goal_id, status="completed"):
        with self._lock:
            for goal in self.goals:
                if goal["id"] == goal_id: goal["status"] = status; return dict(goal)
        return None
goal_manager = GoalManager()
