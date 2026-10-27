class FeedbackEngine:

    def evaluate(self, agent, result):

        return {
            "agent": agent,
            "status": "success",
            "result": result
        }

feedback_engine = FeedbackEngine()