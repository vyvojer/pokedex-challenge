import django_filters
from pokemons.models import Ability, Pokemon, Type


class PokemonFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("name", "name"),
        )
    )

    class Meta:
        model = Pokemon
        fields = {
            "id": ["contains"],
            "name": ["icontains"],
            "types__name": ["icontains"],
            "abilities__name": ["icontains"],
        }


class TypeFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("name", "name"),
        )
    )

    class Meta:
        model = Type
        fields = {
            "id": ["contains"],
            "name": ["icontains"],
        }


class AbilityFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("name", "name"),
        )
    )

    class Meta:
        model = Ability
        fields = {
            "id": ["contains"],
            "name": ["icontains"],
        }
