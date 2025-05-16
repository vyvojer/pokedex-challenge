# The module contains business logic that is directly tied to app
import re
from typing import List

from django.conf import settings
from django.http import HttpRequest
from pokemons.models import Pokemon


def change_filter_ordering(ordering: str | None, field: str) -> str:
    """
    Change the ordering of filters based on the given field.

    This function modifies the ordering string by adding, removing, or toggling
    the sort direction of the specified field.

    Args:
        ordering: Current ordering string, comma-separated list of fields.
            Fields prefixed with '-' are sorted in descending order.
            Can be None if no ordering is currently applied.
        field: The field to modify in the ordering.

    Returns:
        str: Modified ordering string.
    """
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
    Class to manage a session of Pokemon comparisons.

    This class keeps track of Pokemon IDs for comparison in the user session.
    It uses Django's session framework for persistence between requests.

    Attributes:
        SESSION_KEY: Key used to store Pokemon IDs in the session.
        request: The HTTP request object containing the session.
        max_number: Maximum number of Pokemon that can be compared at once.
    """

    SESSION_KEY = "pokemon_comparison_ids"

    def __init__(
        self,
        request: HttpRequest,
        max_number: int = settings.COMPARISON_MAX_POKEMON_NUMBER,
    ):
        """
        Initialize the Pokemon comparison information.

        Args:
            request: The HTTP request object containing the session.
            max_number: Maximum number of Pokemon that can be compared at once.
                Defaults to the value defined in settings.
        """
        self.request = request
        self.max_number = max_number

        if self.SESSION_KEY not in self.request.session:
            self.request.session[self.SESSION_KEY] = []

    @property
    def pokemon_ids(self) -> List[int]:
        """
        Get the list of Pokemon IDs from the session.

        Returns:
            List of Pokemon IDs currently in the comparison.
        """
        return self.request.session.get(self.SESSION_KEY, [])

    @pokemon_ids.setter
    def pokemon_ids(self, value: List[int]) -> None:
        """
        Set the list of Pokemon IDs in the session.

        Args:
            value: List of Pokemon IDs to store in the session.
        """
        self.request.session[self.SESSION_KEY] = value

        if hasattr(self.request.session, "modified"):
            self.request.session.modified = True

    def add_pokemon(self, pokemon_id: int) -> None:
        """
        Add a Pokemon to the comparison.

        This method adds a Pokemon to the comparison if it's not already there
        and if the comparison is not full.

        Args:
            pokemon_id: ID of the Pokemon to add.
        """
        ids = self.pokemon_ids
        if pokemon_id not in ids and not self.is_full():
            ids.append(pokemon_id)
            self.pokemon_ids = ids

    def remove_pokemon(self, pokemon_id: int) -> None:
        """
        Remove a Pokemon from the comparison.

        This method removes a Pokemon from the comparison if it's there.

        Args:
            pokemon_id: ID of the Pokemon to remove.
        """
        ids = self.pokemon_ids
        if pokemon_id in ids:
            ids.remove(pokemon_id)
            self.pokemon_ids = ids

    def get_pokemons(self) -> list[Pokemon]:
        pokemons = [Pokemon.objects.get(id=id) for id in self.pokemon_ids]
        return pokemons

    def is_full(self) -> bool:
        return len(self.pokemon_ids) >= self.max_number
