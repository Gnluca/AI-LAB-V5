from collections import deque
from threading import RLock
class TaskQueue:
    def __init__(self): self.tasks, self._lock = deque(), RLock()
    def enqueue(self, task):
        if not isinstance(task, str) or not task.strip(): raise ValueError("task must be non-empty")
        with self._lock: self.tasks.append(task)
    def dequeue(self):
        with self._lock: return self.tasks.popleft() if self.tasks else None
    def size(self):
        with self._lock: return len(self.tasks)
    def all(self):
        with self._lock: return list(self.tasks)
task_queue = TaskQueue()
