class ModelSelector:

    def select(self, resources):

        cpu = resources["cpu"]["usage"]
        ram = resources["memory"]["usage"]

        models = resources["ollama"]["models"]

        if cpu > 85:
            if "phi3:latest" in models:
                return "phi3:latest"

        if ram > 85:
            if "phi3:latest" in models:
                return "phi3:latest"

        if "llama3.1:latest" in models:
            return "llama3.1:latest"

        if "nimble:latest" in models:
            return "nimble:latest"

        if len(models) > 0:
            return models[0]

        return None


model_selector = ModelSelector()