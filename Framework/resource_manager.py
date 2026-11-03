try:
    from .providers.cpu_provider import cpu_provider
    from .providers.memory_provider import memory_provider
    from .providers.ollama_provider import ollama_provider
except ImportError:
    from providers.cpu_provider import cpu_provider
    from providers.memory_provider import memory_provider
    from providers.ollama_provider import ollama_provider
from providers.node_provider import node_provider

class ResourceManager:

    def collect(self):

        return {
    "cpu": cpu_provider.collect(),
    "memory": memory_provider.collect(),
    "ollama": ollama_provider.collect(),
    "node56": node_provider.collect()
}



resource_manager = ResourceManager()


if __name__ == "__main__":

    data = resource_manager.collect()

    print(data)
