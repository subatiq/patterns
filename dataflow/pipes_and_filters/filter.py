from dataclasses import dataclass
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from multiprocessing import Process, Queue

from PIL.Image import Image


@dataclass
class Frame:
    image: Image
    created_at: datetime


class Filter(Process, ABC):
    def __init__(
        self,
        outputs: list[Queue],
    ):
        super().__init__()
        self.input = Queue()
        self.outputs = outputs

    @abstractmethod
    def _process(self, image: Image) -> Image:
        raise NotImplementedError

    def run(self) -> None:
        while True:
            data = self.input.get()
            lag = (datetime.now() - data.created_at).total_seconds() * 1000
            print(self.__class__.__name__, f'{lag}ms')

            image = self._process(data.image)

            for output in self.outputs:
                output.put(Frame(image=image, created_at=data.created_at))

