class ModelSelector:
    PREFERRED = ("llama3.1:latest", "nimble:latest", "phi3:latest")

    @staticmethod
    def _number(value):
        try: return float(value)
        except (TypeError, ValueError): return None

    def select(self, resources=None):
        resources = resources or {}
        cpu = self._number((resources.get("cpu") or {}).get("usage"))
        ram = self._number((resources.get("memory") or {}).get("usage"))
        ollama = resources.get("ollama") or {}
        models = [str(m) for m in (ollama.get("models") or []) if m]
        if not models: return None
        if ((cpu is not None and cpu > 85) or (ram is not None and ram > 85)) and "phi3:latest" in models:
            return "phi3:latest"
        for model in self.PREFERRED:
            if model in models: return model
        return models[0]

model_selector = ModelSelector()
