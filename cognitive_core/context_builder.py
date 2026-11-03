def build_context(observation):

    context = {
        "status": "healthy",
        "problems": [],
        "recommendations": []
    }

    cpu = observation["cpu"]["usage"]
    ram = observation["memory"]["usage"]

    if cpu > 85:

        context["status"] = "warning"

        context["problems"].append(
            f"CPU elevata ({cpu}%)"
        )

    if ram > 85:

        context["status"] = "warning"

        context["problems"].append(
            f"RAM elevata ({ram}%)"
        )

    if observation["ollama"]["status"] != "online":

        context["status"] = "critical"

        context["problems"].append(
            "Ollama offline"
        )

    if observation["node56"] != "online":

        context["status"] = "warning"

        context["problems"].append(
            "Node56 offline"
        )

    if not context["problems"]:

        context["recommendations"].append(
            "Sistema stabile"
        )

    return context


if __name__ == "__main__":

    sample = {
        "cpu": {
            "usage": 15
        },
        "memory": {
            "usage": 42
        },
        "ollama": {
            "status": "online"
        },
        "node56": "online"
    }

    print(
        build_context(sample)
    )