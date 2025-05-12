import re
from abc import ABC, abstractmethod


class BaseTransformer(ABC):
    def __init__(self, data: dict, **kwargs: dict):
        self.data = data
        self.kwargs = kwargs

    @abstractmethod
    def transform(self) -> dict:
        raise NotImplementedError


def get_id_from_url(url: str) -> int:
    match = re.search(r"/(\d+)/$", url)
    if not match:
        raise ValueError(f"Can't extract id from url: {url}")
    return int(match.group(1))


class PokemonTransformer(BaseTransformer):
    def transform(self) -> dict:
        types = [
            {
                "slot": t["slot"],
                "type": {
                    "id": get_id_from_url(t["type"]["url"]),
                    "name": t["type"]["name"],
                },
            }
            for t in self.data["types"]
        ]
        return {
            "id": self.data["id"],
            "name": self.data["name"],
            "types": types,
        }
