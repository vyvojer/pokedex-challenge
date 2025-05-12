from unittest import TestCase
from unittest.mock import Mock, patch

import requests

from core.integrations.loaders import EntityLoader, LoaderException, PageLoader


@patch("core.integrations.loaders.requests.get")
class PageLoaderTest(TestCase):
    def test_load_pokemons__has_next_url__returns_ids_and_next_url(self, mocked_get):
        response_data = {
            "count": 1302,
            "next": "https://pokeapi.co/api/v2/pokemon/?offset=20&limit=20",
            "previous": None,
            "results": [
                {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
                {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
                {"name": "venusaur", "url": "https://pokeapi.co/api/v2/pokemon/3/"},
                {"name": "charmander", "url": "https://pokeapi.co/api/v2/pokemon/4/"},
            ],
        }
        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=response_data)
        )

        loader = PageLoader(url="https://pokeapi.co/api/v2/pokemon/")
        entity_urls, next_url = loader.load()

        self.assertEqual(
            entity_urls,
            [
                "https://pokeapi.co/api/v2/pokemon/1/",
                "https://pokeapi.co/api/v2/pokemon/2/",
                "https://pokeapi.co/api/v2/pokemon/3/",
                "https://pokeapi.co/api/v2/pokemon/4/",
            ],
        )

        self.assertEqual(
            next_url, "https://pokeapi.co/api/v2/pokemon/?offset=20&limit=20"
        )

        mocked_get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/")

    def test_load_pokemons__next_url_is_null__returns_next_url_none(self, mocked_get):
        response_data = {
            "count": 1302,
            "next": None,
            "previous": None,
            "results": [
                {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
            ],
        }
        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=response_data)
        )

        loader = PageLoader(url="https://pokeapi.co/api/v2/pokemon/")
        entity_urls, next_url = loader.load()

        self.assertEqual(next_url, None)

        mocked_get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/")

    def test_load_pokemons__status_is_not_200__raise_loader_exception(self, mocked_get):
        mocked_get.return_value = Mock(status_code=500, json=Mock(return_value={}))

        loader = PageLoader(url="https://pokeapi.co/api/v2/pokemon/")

        with self.assertRaises(LoaderException):
            loader.load()

    def test_load_pokemons__requests_raise_exeption__raise_loader_exception(
        self, mocked_get
    ):
        mocked_get.side_effect = requests.exceptions.RequestException()

        loader = PageLoader(url="https://pokeapi.co/api/v2/pokemon/")

        with self.assertRaises(LoaderException):
            loader.load()


@patch("core.integrations.loaders.requests.get")
class EntityLoaderTest(TestCase):
    def test_load__status_200__returns_data(self, mocked_get):
        response_data = {
            "name": "bulbasaur",
            "types": [
                {"name": "grass"},
                {"name": "poison"},
            ],
        }
        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=response_data)
        )

        loader = EntityLoader(url="https://pokeapi.co/api/v2/pokemon/1/")
        result = loader.load()

        self.assertEqual(result, response_data)

        mocked_get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/1/")
