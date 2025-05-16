from unittest.mock import Mock, patch

from django.test import TestCase, override_settings
from pokemons.models import Ability, Pokemon, Type

from core.integrations.tasks import load_entity_task, save_entity_task


@patch("core.integrations.loaders.requests.get")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class LoadEntityTaskSaveEntityTaskChainTest(TestCase):
    def setUp(self):
        self.data = {
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

    def test_chain__creates_pokemon_types_and_abilities(self, mocked_get):
        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=self.data)
        )
        source = "pokemon"
        url = "https://pokeapi.co/api/v2/pokemon/42/"

        chain = load_entity_task.si(url, source) | save_entity_task.s(source)

        chain.delay()

        self.assertEqual(Pokemon.objects.count(), 1)
        self.assertEqual(Ability.objects.count(), 1)
        self.assertEqual(Type.objects.count(), 2)
