from unittest import TestCase

from core.integrations.transformers import PokemonTransformer


class PokemonTransformerTest(TestCase):
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
        }

        transformer = PokemonTransformer(data=source_data)
        transformed_data = transformer.transform()
        expected_data = {
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

        self.assertEqual(transformed_data, expected_data)
