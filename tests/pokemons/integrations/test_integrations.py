# Integration tests
from unittest import skip
from unittest.mock import Mock, patch

from django.test import TestCase, override_settings
from pokemons.models import Pokemon, Type

from core.integrations.tasks import load_page_task, sync_data


@patch("core.integrations.loaders.requests.get")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class PokemonSyncDataTest(TestCase):
    def setUp(self):
        self.page_1_data = {
            "count": 4,
            "next": "https://pokeapi.co/api/v2/pokemon/?offset=2&limit=2",
            "previous": None,
            "results": [
                {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
                {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
            ],
        }

        self.page_2_data = {
            "count": 4,
            "next": None,
            "previous": "https://pokeapi.co/api/v2/pokemon/?offset=0&limit=2",
            "results": [
                {"name": "venusaur", "url": "https://pokeapi.co/api/v2/pokemon/3/"},
                {"name": "charmander", "url": "https://pokeapi.co/api/v2/pokemon/4/"},
            ],
        }

        self.entity_1_data = {
            "id": 1,
            "name": "bulbasaur",
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
        }

        self.entity_2_data = {
            "id": 2,
            "name": "ivysaur",
            "types": [
                {
                    "slot": 1,
                    "type": {
                        "name": "grass",
                        "url": "https://pokeapi.co/api/v2/type/12/",
                    },
                },
            ],
        }

        self.entity_3_data = {
            "id": 3,
            "name": "venusaur",
            "types": [
                {
                    "slot": 1,
                    "type": {
                        "name": "poison",
                        "url": "https://pokeapi.co/api/v2/type/4/",
                    },
                },
            ],
        }

        self.entity_4_data = {
            "id": 4,
            "name": "charmander",
            "types": [
                {
                    "slot": 1,
                    "type": {
                        "name": "fire",
                        "url": "https://pokeapi.co/api/v2/type/10/",
                    },
                }
            ],
        }

    @skip
    def test_load_page_task__no_entities__creates_entities(self, mocked_get: Mock):

        mocked_get.side_effect = lambda url: {
            "https://pokeapi.co/api/v2/pokemon/": Mock(
                status_code=200, json=Mock(return_value=self.page_1_data)
            ),
            "https://pokeapi.co/api/v2/pokemon/?offset=2&limit=2": Mock(
                status_code=200, json=Mock(return_value=self.page_2_data)
            ),
            "https://pokeapi.co/api/v2/pokemon/1/": Mock(
                status_code=200, json=Mock(return_value=self.entity_1_data)
            ),
            "https://pokeapi.co/api/v2/pokemon/2/": Mock(
                status_code=200, json=Mock(return_value=self.entity_2_data)
            ),
            "https://pokeapi.co/api/v2/pokemon/3/": Mock(
                status_code=200, json=Mock(return_value=self.entity_3_data)
            ),
            "https://pokeapi.co/api/v2/pokemon/4/": Mock(
                status_code=200, json=Mock(return_value=self.entity_4_data)
            ),
        }[url]

        load_page_task.apply("pokemon")

        self.assertEqual(Pokemon.objects.count(), 4)
