import django_filters
from pokemons.models import Pokemon


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
        }
