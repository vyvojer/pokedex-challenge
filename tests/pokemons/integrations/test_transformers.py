from unittest import TestCase

from pokemons.integrations.transformers import AbilityTransformer, PokemonTransformer


class PokemonTransformerTest(TestCase):
    maxDiff = None

    def test_transform__returns_data(self):
        source_data = {
            "id": 42,
            "name": "bulbasaur",
            "abilities": [
                {
                    "ability": {
                        "name": "overgrow",
                        "url": "https://pokeapi.co/api/v2/ability/65/",
                    },
                    "is_hidden": False,
                    "slot": 1,
                },
            ],
            "types": [
                {
                    "slot": 1,
                    "type": {
                        "name": "grass",
                        "url": "https://pokeapi.co/api/v2/type/12/",
                    },
                },
                {
                    "slot": 2,
                    "type": {
                        "name": "poison",
                        "url": "https://pokeapi.co/api/v2/type/4/",
                    },
                },
            ],
            "weight": 69,
            "height": 3,
            "sprites": {
                "back_default": None,
                "back_female": None,
                "back_shiny": None,
                "back_shiny_female": None,
                "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/10276.png",
                "front_female": None,
                "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/10276.png",
                "front_shiny_female": None,
            },
        }

        transformer = PokemonTransformer(data=source_data)
        transformed_data = transformer.transform()
        expected_data = {
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

        self.assertEqual(transformed_data, expected_data)


class AbilityTransformerTest(TestCase):
    def test_transform__returns_data(self):
        source_data = {
            "generation": {
                "name": "generation-iii",
                "url": "https://pokeapi.co/api/v2/generation/3/",
            },
            "id": 2,
            "is_main_series": True,
            "name": "drizzle",
        }

        transformer = AbilityTransformer(data=source_data)
        transformed_data = transformer.transform()
        expected_data = {
            "id": 2,
            "name": "drizzle",
            "is_main_series": True,
        }

        self.assertEqual(transformed_data, expected_data)
