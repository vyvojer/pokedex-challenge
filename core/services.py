# The module contains business logic that isn't directly tied to a specific app's models
import json

from django.conf import settings
from django_celery_beat.models import IntervalSchedule, PeriodicTask


def create_periodic_tasks():
    """
    Create periodic tasks for data synchronization.

    This function creates daily interval tasks for each data source defined in settings.DATA_SOURCES.
    Each task is created only if it doesn't already exist.
    """
    interval, _ = IntervalSchedule.objects.get_or_create(
        every=24,
        period=IntervalSchedule.HOURS,
    )

    for source in settings.DATA_SOURCES:
        if not PeriodicTask.objects.filter(name=f"Update {source}").exists():
            PeriodicTask.objects.create(
                name=f"Update {source}",
                task="core.integrations.tasks.sync_data",
                interval=interval,
                enabled=False,
                kwargs=json.dumps({"source": source}),
            )
