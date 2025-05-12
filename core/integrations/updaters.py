from abc import ABC, abstractmethod

from django.apps import apps
from django.db import IntegrityError
from django.db.models import Model
from pokemons.models import PokemonType, Type


class BaseUpdater(ABC):
    MANY_TO_MANY_FIELDS = []

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
            if field not in self.MANY_TO_MANY_FIELDS
        }
        self.instance = self.create_or_update_without_race_condition(
            self.model, model_data
        )
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

    @abstractmethod
    def handle_many_to_many_fields(self) -> None:
        raise NotImplementedError


class PokemonUpdater(BaseUpdater):
    MANY_TO_MANY_FIELDS = ["types"]

    def handle_many_to_many_fields(self) -> None:
        for type_slot_data in self.data["types"]:
            slot = type_slot_data["slot"]
            type_data = type_slot_data["type"]
            type_ = self.create_or_update_without_race_condition(
                model=Type, data=type_data
            )
            PokemonType.objects.update_or_create(
                pokemon=self.instance,
                type=type_,
                defaults={"slot": slot},
            )
