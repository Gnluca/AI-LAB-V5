import subprocess


class OllamaProvider:

    def collect(self):

        try:

            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )

            models = []

            lines = result.stdout.splitlines()

            for line in lines[1:]:

                if line.strip():

                    model = line.split()[0]

                    models.append(model)

            return {
                "resource": "ollama",
                "models": models,
                "status": "online"
            }

        except Exception as e:

            return {
                "resource": "ollama",
                "models": [],
                "status": "offline",
                "error": str(e)
            }


ollama_provider = OllamaProvider()