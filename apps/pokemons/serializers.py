from pokemons.models import Ability, Pokemon, Type
from rest_framework import serializers


class TypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Type model.
    """

    class Meta:
        model = Type
        fields = "__all__"


class AbilitySerializer(serializers.ModelSerializer):
    """
    Serializer for the Ability model.
    """

    class Meta:
        model = Ability
        fields = "__all__"


class PokemonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Pokemon model.

    Attributes:
        types: Nested TypeSerializer instances for the Pokemon's types.
    """

    types = TypeSerializer(many=True, read_only=True)

    class Meta:
        model = Pokemon
        fields = "__all__"
