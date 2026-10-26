from datetime import datetime

AGENT_PRIORITIES = {
    "LabManager": 100,
    "MemoryAgent": 90,
    "KnowledgeAgent": 85,
    "NetworkAgent": 80,
    "HardwareAgent": 75,
    "SchedulerAgent": 70,
    "DevelopmentAgent": 65
}

EXECUTION_POLICIES = {
    "allow_parallel_tasks": True,
    "max_concurrent_agents": 4,
    "retry_failed_tasks": True,
    "max_retries": 3,
    "task_timeout": 300
}

ERROR_POLICIES = {
    "INFO": 0,
    "WARNING": 1,
    "ERROR": 2,
    "CRITICAL": 3
}


def get_governance():
    return {
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "version": "6.3",
        "priorities": AGENT_PRIORITIES,
        "policies": EXECUTION_POLICIES,
        "errors": ERROR_POLICIES
    }