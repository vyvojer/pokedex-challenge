from django.test import SimpleTestCase, override_settings
from pokemons.models import Pokemon

from core.integrations.factories import DataSourceFactory
from core.integrations.loaders import DefaultEntityLoader, DefaultPageLoader
from core.integrations.transformers import BaseTransformer
from core.integrations.updaters import DefaultUpdater


class DummyTransformer(BaseTransformer):

    def transform(self) -> dict:
        return {}


class DummyUpdater(DefaultUpdater):
    def handle_many_to_many_fields(self) -> None:
        pass


# Test settings for DATA_SOURCES
TEST_DATA_SOURCES = {
    "test_source": {
        "page_loader": {
            "class": "core.integrations.loaders.DefaultPageLoader",
            "kwargs": {"url": "https://test-api.com/items/"},
        },
        "entity_loader": {
            "class": "core.integrations.loaders.DefaultEntityLoader",
            "kwargs": {"extra_param": "value"},
        },
        "transformer": {
            "class": "tests.core.integrations.test_factories.DummyTransformer",
            "kwargs": {"extra_param": "value"},
        },
        "updater": {
            "class": "tests.core.integrations.test_factories.DummyUpdater",
            "kwargs": {"model_name": "pokemons.Pokemon"},
        },
    }
}


class DataSourceFactoryTest(SimpleTestCase):

    @override_settings(DATA_SOURCES=TEST_DATA_SOURCES)
    def test_get_page_loader__without_url__returns_loader_instance_with_initial_url(
        self,
    ):
        factory = DataSourceFactory("test_source")
        loader = factory.get_page_loader()

        self.assertTrue(isinstance(loader, DefaultPageLoader))
        self.assertEqual(loader.url, "https://test-api.com/items/")

    @override_settings(DATA_SOURCES=TEST_DATA_SOURCES)
    def test_get_page_loader__with_url__returns_loader_instance_with_url(self):
        factory = DataSourceFactory("test_source")
        custom_page_url = "https://test-api.com/items/?offset=20&limit=20"
        loader = factory.get_page_loader(url=custom_page_url)

        self.assertEqual(loader.url, custom_page_url)

    @override_settings(DATA_SOURCES=TEST_DATA_SOURCES)
    def test_get_entity_loader__returns_entity_loader_instance_with_url(self):
        factory = DataSourceFactory("test_source")
        url = "https://test-api.com/items/123/"
        loader = factory.get_entity_loader(url=url)

        self.assertTrue(isinstance(loader, DefaultEntityLoader))
        self.assertEqual(loader.url, url)

    @override_settings(DATA_SOURCES=TEST_DATA_SOURCES)
    def test_get_transformer__returns_transformer_instance_with_data_and_kwargs(self):
        factory = DataSourceFactory("test_source")
        data = {"id": 1, "name": "test_pokemon", "types": []}
        transformer = factory.get_transformer(data=data)

        self.assertTrue(isinstance(transformer, DummyTransformer))
        self.assertEqual(transformer.data, data)
        self.assertEqual(transformer.kwargs["extra_param"], "value")

    @override_settings(DATA_SOURCES=TEST_DATA_SOURCES)
    def test_get_updater__returns_updater_instance_with_data(self):
        factory = DataSourceFactory("test_source")
        data = {"id": 1, "name": "test_pokemon", "types": []}
        updater = factory.get_updater(data=data)

        self.assertTrue(isinstance(updater, DummyUpdater))
        self.assertEqual(updater.data, data)
        self.assertEqual(updater.model, Pokemon)
