from models.task_model import Task
from ports.task_storage import InMemoryTaskStorage, TaskStorage


in_memory = InMemoryTaskStorage()


def add_task(repo: TaskStorage, task: Task):
    repo.save(task)

