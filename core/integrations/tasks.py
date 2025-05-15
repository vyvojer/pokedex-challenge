import logging
from typing import Any

from celery import group, shared_task

from core.integrations.factories import DataSourceFactory
from core.integrations.loaders import LoaderException

logger = logging.getLogger(__name__)


@shared_task
def sync_data(source: str) -> None:
    load_page_task.delay(source)


@shared_task(
    bind=True,
    autoretry_for=(LoaderException,),
    retry_backoff=True,  # exponential
    retry_kwargs={"max_retries": 5},
)
def load_page_task(self, source: str, page_url: str | None = None) -> None:
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
    """Download a single entity and return the *raw* JSON payload."""
    factory = DataSourceFactory(source)
    entity_data = factory.get_entity_loader(url=entity_url).load()
    return entity_data


@shared_task
def save_entity_task(entity_data: dict[str, Any], source: str) -> None:
    """Apply the transformer, then upsert into Django via the updater."""
    factory = DataSourceFactory(source)

    transformed = factory.get_transformer(data=entity_data).transform()
    factory.get_updater(data=transformed).create_or_update()
