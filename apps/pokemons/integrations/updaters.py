from pokemons.models import Ability, PokemonAbility, PokemonType, Type

from core.integrations.updaters import DefaultUpdater


class PokemonUpdater(DefaultUpdater):
    many_to_many_fields = ["types", "abilities"]

    def handle_many_to_many_fields(self) -> None:
        for ability_slot_data in self.data["types"]:
            slot = ability_slot_data["slot"]
            ability_data = ability_slot_data["type"]
            type_ = self.create_or_update_without_race_condition(
                model=Type, data=ability_data
            )
            PokemonType.objects.update_or_create(
                pokemon=self.instance,
                type=type_,
                defaults={"slot": slot},
            )

        for ability_slot_data in self.data["abilities"]:
            slot = ability_slot_data["slot"]
            is_hidden = ability_slot_data["is_hidden"]
            ability_data = ability_slot_data["ability"]
            ability = self.create_or_update_without_race_condition(
                model=Ability, data=ability_data
            )
            PokemonAbility.objects.update_or_create(
                pokemon=self.instance,
                ability=ability,
                defaults={"slot": slot, "is_hidden": is_hidden},
            )
