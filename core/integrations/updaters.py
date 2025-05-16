from django.apps import apps
from django.db import IntegrityError
from django.db.models import Model


class DefaultUpdater:
    """
    Default implementation for creating or updating model instances.

    This class provides functionality to create or update Django model instances
    based on provided data, handling race conditions and many-to-many relationships.
    """

    many_to_many_fields = []
    fk_fields = []

    def __init__(self, model_name: str, data: dict, **kwargs: dict):
        """
        Initialize the updater with a model name, data, and optional parameters.

        Args:
            model_name: The name of the model in the format "app_label.model_name"
            data: The data to use for creating or updating the model instance
            **kwargs: Additional parameters to use during the update process
        """
        self.data = data
        app_label, model_name = model_name.split(".")
        self.model = apps.get_model(app_label, model_name)
        self.kwargs = kwargs
        self.instance = None

    def create_or_update(self) -> None:
        """
        Create or update a model instance with the provided data.

        This method extracts the relevant fields from the data, excluding many-to-many fields,
        and creates or updates a model instance. If many-to-many fields are present,
        they are handled separately after the instance is created or updated.
        """
        model_data = {
            field: self.data[field]
            for field in self.data
            if field not in self.many_to_many_fields
        }
        self.instance = self.create_or_update_without_race_condition(
            self.model, model_data
        )
        if self.many_to_many_fields:
            self.handle_many_to_many_fields()

    @staticmethod
    def create_or_update_without_race_condition(model: type, data: dict) -> Model:
        """
        Create or update a model instance while preventing race conditions.

        This method uses select_for_update to lock the row during update operations,
        preventing race conditions when multiple processes try to create or update
        the same instance simultaneously.

        Args:
            model: The Django model class
            data: The data to use for creating or updating the model instance

        Returns:
            The created or updated model instance
        """
        if model.objects.filter(id=data["id"]).exists():
            model.objects.select_for_update().filter(id=data["id"]).update(**data)
            instance = model.objects.get(id=data["id"])
        else:
            try:  # preventing race condition for model creating
                instance = model.objects.create(**data)
            except IntegrityError as e:
                model.objects.select_for_update().filter(id=data["id"]).update(**data)
                instance = model.objects.get(id=data["id"])
        return instance

    def handle_many_to_many_fields(self) -> None:
        """
        Handle many-to-many relationships for the model instance.

        This method is a placeholder that should be overridden by subclasses
        to implement specific logic for handling many-to-many relationships.
        The default implementation does nothing.
        """
        pass
