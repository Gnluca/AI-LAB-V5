from core.manager import LabManager

manager = LabManager()

manager.register_agent("DevelopmentAgent")
manager.register_agent("NetworkAgent")
manager.register_agent("HardwareAgent")

manager.register_node("192.168.1.41")
manager.register_node("192.168.1.56")

print(manager.get_status())
