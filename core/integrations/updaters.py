from django.apps import apps
from django.db import IntegrityError
from django.db.models import Model


class DefaultUpdater:
    many_to_many_fields = []
    fk_fields = []

    def __init__(self, model_name: str, data: dict, **kwargs: dict):
        self.data = data
        app_label, model_name = model_name.split(".")
        self.model = apps.get_model(app_label, model_name)
        self.kwargs = kwargs
        self.instance = None

    def create_or_update(self) -> None:
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
        pass
