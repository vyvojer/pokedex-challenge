from abc import ABC, abstractmethod
from typing import Any, TypedDict


class PageResult(TypedDict):
    results: list[Any]
    next_url: str | None


class BaseLoader(ABC):
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    @abstractmethod
    def load(self) -> PageResult:
        raise NotImplementedError
