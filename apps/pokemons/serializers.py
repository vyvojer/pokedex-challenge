from pokemons.models import Pokemon, Type
from rest_framework import serializers


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class PokemonSerializer(serializers.ModelSerializer):
    types = TypeSerializer(many=True, read_only=True)

    class Meta:
        model = Pokemon
        fields = "__all__"
