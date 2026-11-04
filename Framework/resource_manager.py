from __future__ import annotations

from .providers.cpu_provider import cpu_provider
from .providers.memory_provider import memory_provider
from .providers.ollama_provider import ollama_provider
from .providers.node_provider import node_provider

class ResourceManager:
    """Collect resources independently so a failed provider doesn't abort observation."""
    def __init__(self, providers=None):
        self.providers = providers or {
            "cpu": cpu_provider, "memory": memory_provider,
            "ollama": ollama_provider, "node56": node_provider,
        }

    def collect(self):
        result = {}
        for name, provider in self.providers.items():
            try:
                value = provider.collect()
                result[name] = value if isinstance(value, dict) else {
                    "resource": name, "status": "error", "error": "Provider result must be a dict"
                }
            except Exception as exc:
                result[name] = {"resource": name, "status": "error", "error": f"{type(exc).__name__}: {exc}"}
        return result

resource_manager = ResourceManager()
