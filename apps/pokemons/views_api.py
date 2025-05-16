from pokemons.models import Ability, Pokemon, Type
from pokemons.serializers import AbilitySerializer, PokemonSerializer, TypeSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView


class TypeListAPIView(ListAPIView):
    """
    API view that returns a list of all Pokemon types.

    This view provides a paginated list of all Pokemon types in the database.

    Attributes:
        queryset: All Type objects.
        serializer_class: The serializer class used to convert Type objects to JSON.
    """

    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class TypeDetailAPIView(RetrieveAPIView):
    """
    API view that returns details of a specific Pokemon type.

    This view provides detailed information about a specific Pokemon type.

    Attributes:
        queryset: All Type objects.
        serializer_class: The serializer class used to convert Type objects to JSON.
    """

    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class PokemonListView(ListAPIView):
    """
    API view that returns a list of all Pokemon.

    This view provides a paginated list of all Pokemon in the database,
    with types prefetched to optimize performance.

    Attributes:
        queryset: All Pokemon objects with prefetched related objects.
        serializer_class: The serializer class used to convert Pokemon objects to JSON.
    """

    queryset = Pokemon.objects.prefetched()
    serializer_class = PokemonSerializer


class PokemonDetailView(RetrieveAPIView):
    """
    API view that returns details of a specific Pokemon.

    This view provides detailed information about a specific Pokemon,
    with types prefetched to optimize performance.

    Attributes:
        queryset: All Pokemon objects with prefetched related objects.
        serializer_class: The serializer class used to convert Pokemon objects to JSON.
    """

    queryset = Pokemon.objects.prefetched()
    serializer_class = PokemonSerializer


class AbilityListAPIView(ListAPIView):
    """
    API view that returns a list of all Pokemon abilities.

    This view provides a paginated list of all Pokemon abilities in the database.

    Attributes:
        queryset: All Ability objects.
        serializer_class: The serializer class used to convert Ability objects to JSON.
    """

    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer


class AbilityDetailAPIView(RetrieveAPIView):
    """
    API view that returns details of a specific Pokemon ability.

    This view provides detailed information about a specific Pokemon ability.

    Attributes:
        queryset: All Ability objects.
        serializer_class: The serializer class used to convert Ability objects to JSON.
    """

    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer
