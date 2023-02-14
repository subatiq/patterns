from uuid import UUID
from dataclasses import dataclass

@dataclass
class Task:
    id: UUID
    pub_id: UUID
    name: str
    completed: bool

    def complete(self):
        self.completed = True
