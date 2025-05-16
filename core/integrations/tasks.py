import logging
from typing import Any

from celery import group, shared_task

from core.integrations.factories import DataSourceFactory
from core.integrations.loaders import LoaderException

logger = logging.getLogger(__name__)


@shared_task
def sync_data(source: str) -> None:
    """
    Start the data synchronization process for a specific data source.

    This is the entry point for the data synchronization process. It initiates
    the asynchronous loading of the first page of data from the specified source.

    Args:
        source: The identifier of the data source  defined in settings.DATA_SOURCES to synchronize
    """
    load_page_task.delay(source)


@shared_task(
    bind=True,
    autoretry_for=(LoaderException,),
    retry_backoff=True,  # exponential
    retry_kwargs={"max_retries": 5},
)
def load_page_task(self, source: str, page_url: str | None = None) -> None:
    """
    Load a page of data from the specified source and process each entity.

    This task loads a page of data from the specified source, extracts entity URLs,
    and creates a group of tasks to load and save each entity. If there is a next page,
    it recursively schedules itself to load that page.

    The task will automatically retry up to 5 times with exponential backoff if a
    LoaderException occurs.

    Args:
        self: The task instance (provided by Celery when bind=True)
        source: The identifier of the data source
        page_url: The URL of the page to load, or None for the first page
    """
    factory = DataSourceFactory(source)
    entity_urls, next_url = factory.get_page_loader(url=page_url).load()

    entity_group = group(
        load_entity_task.si(url, source) | save_entity_task.s(source)
        for url in entity_urls
    )

    if next_url is None:
        canvas = entity_group
    else:
        canvas = group(
            entity_group, load_page_task.si(source, next_url)  # add recurse invoke
        )

        self.replace(canvas)


@shared_task(
    ignore_result=False,
)
def load_entity_task(
    entity_url: str,
    source: str,
) -> dict[str, Any]:
    """
    Download data for a single entity and return the raw JSON payload.

    This task loads data for a specific entity from the given URL using the
    appropriate entity loader for the specified source.

    Args:
        entity_url: The URL to load the entity data from
        source: The identifier of the data source

    Returns:
        The raw JSON data for the entity as a dictionary
    """
    factory = DataSourceFactory(source)
    entity_data = factory.get_entity_loader(url=entity_url).load()
    return entity_data


@shared_task
def save_entity_task(entity_data: dict[str, Any], source: str) -> None:
    """
    Transform and save entity data to the database.

    This task takes raw entity data, applies the appropriate transformer for the
    specified source to convert it to the application's data model, and then uses
    the appropriate updater to create or update the entity in the database.

    Args:
        entity_data: The raw entity data as a dictionary
        source: The identifier of the data source
    """
    factory = DataSourceFactory(source)

    transformed = factory.get_transformer(data=entity_data).transform()
    factory.get_updater(data=transformed).create_or_update()
