import re

from core.integrations.transformers import BaseTransformer


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
        abilities = [
            {
                "slot": t["slot"],
                "is_hidden": t["is_hidden"],
                "ability": {
                    "id": get_id_from_url(t["ability"]["url"]),
                    "name": t["ability"]["name"],
                },
            }
            for t in self.data["abilities"]
        ]
        return {
            "id": self.data["id"],
            "name": self.data["name"],
            "height": self.data["height"],
            "weight": self.data["weight"],
            "front_sprite": self.data["sprites"]["front_default"],
            "types": types,
            "abilities": abilities,
        }


class AbilityTransformer(BaseTransformer):
    def transform(self) -> dict:
        return {
            "id": self.data["id"],
            "name": self.data["name"],
            "is_main_series": self.data["is_main_series"],
        }
