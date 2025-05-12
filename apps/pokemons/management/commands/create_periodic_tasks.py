from django.core.management.base import BaseCommand

from core.services import create_periodic_tasks


class Command(BaseCommand):
    help = "Creates periodic tasks for data synchronization"

    def handle(self, *args, **options):
        self.stdout.write("Creating periodic tasks...")
        create_periodic_tasks()
        self.stdout.write(self.style.SUCCESS("Successfully created periodic tasks"))
