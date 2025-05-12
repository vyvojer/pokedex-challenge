from django.conf import settings
from django.utils.module_loading import import_string


class DataSourceFactory:
    """
    Factory class that dynamically loads and instantiates classes
    based on the source configuration in settings.UPDATE_SOURCES.
    """

    def __init__(self, source: str):
        """
        Initialize the factory with a specific source.

        Args:
            source: Source identifier to load configurations from settings.UPDATE_SOURCES
        """
        if source not in settings.DATA_SOURCES:
            raise ValueError(f"Source '{source}' not found in settings.UPDATE_SOURCES")

        self.source = source
        self.config = settings.DATA_SOURCES[source]

    def get_page_loader(self, url: str | None = None, **kwargs: dict):
        """
        Get the page loader instance configured for this source.

        Returns:
            An instance of the page loader class
        """
        loader_config = self.config.get("page_loader", {})
        loader_class = import_string(loader_config.get("class"))
        kwargs = loader_config.get("kwargs", {}).copy()

        initial_url = kwargs.pop("url")
        if url is None:
            url = initial_url

        return loader_class(url=url, **kwargs)

    def get_entity_loader(self, url: str):
        """
        Get the entity loader instance configured for this source.

        Args:
            entity_id: The ID of the entity to load

        Returns:
            An instance of the entity loader class
        """
        loader_config = self.config.get("entity_loader", {})
        loader_class = import_string(loader_config.get("class"))
        kwargs = loader_config.get("kwargs", {}).copy()

        return loader_class(url=url, **kwargs)

    def get_transformer(self, data: dict):
        """
        Get the transformer instance configured for this source.

        Returns:
            An instance of the transformer class
        """
        transformer_config = self.config.get("transformer", {})
        transformer_class = import_string(transformer_config.get("class"))
        kwargs = transformer_config.get("kwargs", {})

        return transformer_class(data=data, **kwargs)

    def get_updater(self, data: dict):
        """
        Get the updater instance configured for this source.

        Returns:
            An instance of the updater class
        """
        updater_config = self.config.get("updater", {})
        updater_class = import_string(updater_config.get("class"))
        kwargs = updater_config.get("kwargs", {})

        return updater_class(data=data, **kwargs)
