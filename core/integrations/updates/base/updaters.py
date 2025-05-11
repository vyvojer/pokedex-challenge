from abc import ABC, abstractmethod


class BaseUpdater(ABC):
    @abstractmethod
    def update(self, data: dict) -> None:
        raise NotImplementedError
