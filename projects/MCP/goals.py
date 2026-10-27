class GoalManager:

    def __init__(self):
        self.goals = []

    def create_goal(self, goal):

        item = {
            "id": len(self.goals) + 1,
            "goal": goal,
            "status": "pending"
        }

        self.goals.append(item)

        return item

    def list_goals(self):
        return self.goals

    def complete(self, goal_id):

        for goal in self.goals:

            if goal["id"] == goal_id:
                goal["status"] = "completed"

                return goal

goal_manager = GoalManager()