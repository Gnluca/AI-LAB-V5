from runtime.runtime_state import runtime_state

class RuntimeManager:

    def status(self):
        return runtime_state

    def health(self):
        return {
            "status": "healthy"
        }

runtime = RuntimeManager()