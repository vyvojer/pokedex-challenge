import factory


class TypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "pokemons.Type"

    name = factory.Faker("word")


class PokemonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "pokemons.Pokemon"

    name = factory.Faker("word")

    @factory.post_generation
    def types(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:  # If specific types are passed (via `types=[...]`), use them
            for type_instance in extracted:
                self.types.add(type_instance)
        else:
            self.types.add(TypeFactory(), TypeFactory())
