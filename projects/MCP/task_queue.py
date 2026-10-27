class TaskQueue:

    def __init__(self):
        self.tasks = []

    def enqueue(self, task):

        self.tasks.append(task)

    def dequeue(self):

        if self.tasks:
            return self.tasks.pop(0)

        return None

    def size(self):

        return len(self.tasks)

    def all(self):

        return self.tasks

task_queue = TaskQueue()