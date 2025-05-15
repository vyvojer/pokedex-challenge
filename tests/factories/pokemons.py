import factory


class TypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "pokemons.Type"

    name = factory.Faker("word")


class AbilityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "pokemons.Ability"

    name = factory.Faker("word")


class PokemonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "pokemons.Pokemon"

    name = factory.Faker("word")
