import factory


class TypeFactory(factory.django.DjangoModelFactory):
    """
    Generates and manages instances of the Type model for tests using DjangoModelFactory.

    Provides a mechanism to create realistic test data for the Type model through the use
    of Faker for random data generation.

    Attributes:
        name (str): A randomly generated word to populate the 'name' field of the
            Type model.
    """

    class Meta:
        model = "pokemons.Type"

    name = factory.Faker("word")


class AbilityFactory(factory.django.DjangoModelFactory):
    """
    A factory class for creating Ability objects.

    This factory class is used to generate instances of the Ability model, typically
    for testing purposes. It uses the factory_boy library to automatically create and
    populate instances with valid data. The `name` attribute is populated with a random
    word using the Faker library.

    Attributes:
        name (str): A randomly generated word representing the name of the Ability.
    """

    class Meta:
        model = "pokemons.Ability"

    name = factory.Faker("word")


class PokemonFactory(factory.django.DjangoModelFactory):
    """
    Generates instances of the Pokemon model for testing or seeding purposes.

    This factory is designed to create instances of the `pokemons.Pokemon` model
    using the Factory Boy library. It simplifies the creation of test data by
    automatically generating values for model fields. By utilizing Factory Boy's
    features, such as Faker, it can populate fields with realistic data for
    comprehensive testing scenarios.

    Attributes:
        name (str): A randomly generated word used to populate the name field of
            the Pokemon model.
    """

    class Meta:
        model = "pokemons.Pokemon"

    name = factory.Faker("word")
