import json

from django.test import TestCase, override_settings
from django_celery_beat.models import PeriodicTask

from core.services import create_periodic_tasks


class CreatePeriodicTasksTest(TestCase):
    DATA_SOURCES = {
        "test_source": {
            "page_loader": {
                "class": "core.integrations.loaders.PageLoader",
                "kwargs": {"url": "https://test-api.com/items/"},
            },
            "entity_loader": {
                "class": "core.integrations.loaders.EntityLoader",
                "kwargs": {"extra_param": "value"},
            },
        },
        "another_source": {},
    }

    @override_settings(DATA_SOURCES=DATA_SOURCES)
    def test_create_periodic_task__does_not_exist__creates_task(self):
        create_periodic_tasks()

        self.assertEqual(PeriodicTask.objects.count(), 2)

        task_1 = PeriodicTask.objects.get(name="Update test_source")
        task_2 = PeriodicTask.objects.get(name="Update another_source")

        self.assertEqual(task_1.task, "core.integrations.tasks.sync_data")
        self.assertEqual(json.loads(task_1.kwargs), {"source": "test_source"})
        self.assertEqual(task_1.enabled, False)
