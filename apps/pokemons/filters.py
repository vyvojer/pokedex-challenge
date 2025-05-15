import django_filters
from pokemons.models import Pokemon, Type


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
