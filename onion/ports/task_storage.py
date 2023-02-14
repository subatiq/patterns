from abc import ABC, abstractmethod

from models.task_model import Task


class TaskStorage(ABC):
    @abstractmethod
    def save(self, task: Task):
        raise NotImplementedError


class InMemoryTaskStorage(TaskStorage):
    def __init__(self) -> None:
        super().__init__()

        self.tasks = []

    def save(self, task: Task):
        self.tasks.append(task)
