import re
from typing import List

from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpRequest
from pokemons.models import Pokemon


def change_filter_ordering(ordering: str | None, field: str) -> str:
    if ordering is None:
        ordering = field

    elif field not in ordering:
        ordering = f"{field},{ordering}"

    elif field in ordering:
        if f"-{field}" in ordering:
            new_field_ordering = field
        else:
            new_field_ordering = f"-{field}"

        ordering = re.sub(f"(-*{field},*)", "", ordering)
        ordering = f"{new_field_ordering},{ordering}".rstrip(",")

    return ordering


class PokemonComparisonInformation:
    """
    Class to manage a session of pokemon comparisons.
    Keeps track of pokemon IDs for comparison in the user session.
    Uses Django's session framework for persistence between requests.
    """

    SESSION_KEY = "pokemon_comparison_ids"

    def __init__(
        self,
        request: HttpRequest,
        max_number: int = settings.COMPARISON_MAX_POKEMON_NUMBER,
    ):
        self.request = request
        self.max_number = max_number

        if self.SESSION_KEY not in self.request.session:
            self.request.session[self.SESSION_KEY] = []

    @property
    def pokemon_ids(self) -> List[int]:
        return self.request.session.get(self.SESSION_KEY, [])

    @pokemon_ids.setter
    def pokemon_ids(self, value: List[int]) -> None:
        self.request.session[self.SESSION_KEY] = value

        if hasattr(self.request.session, "modified"):
            self.request.session.modified = True

    def add_pokemon(self, pokemon_id: int) -> None:
        ids = self.pokemon_ids
        if pokemon_id not in ids and not self.is_full():
            ids.append(pokemon_id)
            self.pokemon_ids = ids

    def remove_pokemon(self, pokemon_id: int) -> None:
        ids = self.pokemon_ids
        if pokemon_id in ids:
            ids.remove(pokemon_id)
            self.pokemon_ids = ids

    def get_pokemons(self) -> list[Pokemon]:
        pokemons = [Pokemon.objects.get(id=id) for id in self.pokemon_ids]
        return pokemons

    def is_full(self) -> bool:
        return len(self.pokemon_ids) >= self.max_number
