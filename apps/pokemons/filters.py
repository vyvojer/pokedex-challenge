import django_filters
from pokemons.models import Ability, Pokemon, Type


class PokemonFilter(django_filters.FilterSet):
    """
    Filter for Pokemon model.

    This filter allows filtering Pokemon by name, type name, and ability name,
    as well as ordering by ID and name.

    Attributes:
        o: Ordering filter for ID and name fields.
    """

    o = django_filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("name", "name"),
        )
    )

    class Meta:
        model = Pokemon
        fields = {
            "name": ["icontains"],
            "types__name": ["icontains"],
            "abilities__name": ["icontains"],
        }


class TypeFilter(django_filters.FilterSet):
    """
    Filter for Type model.

    This filter allows filtering Type by name and ordering by ID and name.

    Attributes:
        o: Ordering filter for ID and name fields.
    """

    o = django_filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("name", "name"),
        )
    )

    class Meta:
        model = Type
        fields = {
            "name": ["icontains"],
        }


class AbilityFilter(django_filters.FilterSet):
    """
    Filter for Ability model.

    This filter allows filtering Ability by name and ordering by ID and name.

    Attributes:
        o: Ordering filter for ID and name fields.
    """

    o = django_filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("name", "name"),
        )
    )

    class Meta:
        model = Ability
        fields = {
            "name": ["icontains"],
        }
