from runtime.factory import factory

from agents.memory_agent import MemoryAgent
from agents.network_agent import NetworkAgent
from agents.hardware_agent import HardwareAgent
from agents.knowledge_agent import KnowledgeAgent

factory.register(MemoryAgent())
factory.register(NetworkAgent())
factory.register(HardwareAgent())
factory.register(KnowledgeAgent())

print(factory.status())