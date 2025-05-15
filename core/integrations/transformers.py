import re
from abc import ABC, abstractmethod


class BaseTransformer(ABC):
    def __init__(self, data: dict, **kwargs: dict):
        self.data = data
        self.kwargs = kwargs

    @abstractmethod
    def transform(self) -> dict:
        raise NotImplementedError
