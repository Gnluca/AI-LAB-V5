import subprocess

class SchedulerAgent:

    def list_tasks(self):

        result = subprocess.run(
            ["schtasks", "/query"],
            capture_output=True,
            text=True
        )

        return result.stdout