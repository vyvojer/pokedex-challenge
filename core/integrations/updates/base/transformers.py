from abc import ABC, abstractmethod


class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, data: dict) -> dict:
        raise NotImplementedError
