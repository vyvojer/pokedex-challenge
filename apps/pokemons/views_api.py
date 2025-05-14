from pokemons.models import Pokemon, Type
from pokemons.serializers import PokemonSerializer, TypeSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView


class TypeListAPIView(ListAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class TypeDetailAPIView(RetrieveAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class PokemonListView(ListAPIView):
    queryset = Pokemon.objects.prefetched()
    serializer_class = PokemonSerializer


class PokemonDetailView(RetrieveAPIView):
    queryset = Pokemon.objects.prefetched()
    serializer_class = PokemonSerializer
