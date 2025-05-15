import factory


class TypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "pokemons.Type"

    name = factory.Faker("word")


class PokemonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "pokemons.Pokemon"

    name = factory.Faker("word")
