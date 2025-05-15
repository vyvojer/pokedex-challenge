from django.test import TestCase
from pokemons.integrations.updaters import PokemonUpdater
from pokemons.models import Ability, Pokemon, PokemonType, Type

from core.integrations.updaters import DefaultUpdater
from tests.factories.pokemons import AbilityFactory, PokemonFactory


class DefaultUpdaterTestCase(TestCase):
    def setUp(self):
        self.data = {
            "id": 2,
            "name": "drizzle",
            "is_main_series": True,
        }

    def test_update__entity_not_exist__creates_entity(self):
        updater = DefaultUpdater(model_name="pokemons.Ability", data=self.data)
        updater.create_or_update()

        self.assertEqual(Ability.objects.count(), 1)

        ability = Ability.objects.first()

        self.assertEqual(ability.id, 2)
        self.assertEqual(ability.name, "drizzle")
        self.assertEqual(ability.is_main_series, True)

    def test_update__entity_exists__updates_entity(self):
        ability = AbilityFactory(
            id=2,
            name="old_name",
            is_main_series=False,
        )

        updater = DefaultUpdater(model_name="pokemons.Ability", data=self.data)
        updater.create_or_update()

        self.assertEqual(Ability.objects.count(), 1)
        ability.refresh_from_db()

        self.assertEqual(ability.id, 2)
        self.assertEqual(ability.name, "drizzle")
        self.assertEqual(ability.is_main_series, True)


class PokemonUpdaterTestCase(TestCase):
    def setUp(self):
        self.data = {
            "id": 42,
            "name": "bulbasaur",
            "weight": 69,
            "height": 3,
            "front_sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/10276.png",
            "abilities": [
                {
                    "ability": {
                        "id": 65,
                        "name": "overgrow",
                    },
                    "is_hidden": False,
                    "slot": 1,
                },
            ],
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
        self.assertEqual(instance.weight, 69)
        self.assertEqual(instance.height, 3)
        self.assertEqual(
            instance.front_sprite,
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/10276.png",
        )

        self.assertEqual(Type.objects.count(), 2)

        type_12 = Type.objects.get(id=12)
        type_4 = Type.objects.get(id=4)

        self.assertEqual(type_12.name, "grass")
        self.assertEqual(type_4.name, "poison")

        type_pokemon_1 = PokemonType.objects.get(pokemon=instance, type=type_12)
        type_pokemon_2 = PokemonType.objects.get(pokemon=instance, type=type_4)

        self.assertEqual(type_pokemon_1.slot, 1)
        self.assertEqual(type_pokemon_2.slot, 2)

        self.assertEqual(Ability.objects.count(), 1)

        ability = Ability.objects.get(id=65)

    def test_update__entities_exist__updates_entity(self):
        pokemon = PokemonFactory(id=42)
