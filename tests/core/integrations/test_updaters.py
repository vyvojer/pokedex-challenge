from django.test import TestCase
from pokemons.models import Pokemon, PokemonType, Type

from core.integrations.updaters import PokemonUpdater
from factories.pokemons import PokemonFactory


class PokemonUpdaterTestCase(TestCase):
    def setUp(self):
        self.data = {
            "id": 42,
            "name": "bulbasaur",
            "types": [
                {
                    "slot": 1,
                    "type": {
                        "id": 12,
                        "name": "grass",
                    },
                },
                {
                    "slot": 2,
                    "type": {
                        "id": 4,
                        "name": "poison",
                    },
                },
            ],
        }

    def test_update__entities_not_exist__creates_entities(self):
        updater = PokemonUpdater(model_name="pokemons.Pokemon", data=self.data)
        updater.create_or_update()

        self.assertEqual(Pokemon.objects.count(), 1)

        instance = Pokemon.objects.first()

        self.assertEqual(instance.id, 42)
        self.assertEqual(instance.name, "bulbasaur")

        self.assertEqual(Type.objects.count(), 2)

        type_12 = Type.objects.get(id=12)
        type_4 = Type.objects.get(id=4)

        self.assertEqual(type_12.name, "grass")
        self.assertEqual(type_4.name, "poison")

        type_pokemon_1 = PokemonType.objects.get(pokemon=instance, type=type_12)
        type_pokemon_2 = PokemonType.objects.get(pokemon=instance, type=type_4)

        self.assertEqual(type_pokemon_1.slot, 1)
        self.assertEqual(type_pokemon_2.slot, 2)

    def test_update__entities_exist__updates_entity(self):
        pokemon = PokemonFactory(id=42)
