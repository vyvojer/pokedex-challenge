from django.db import models
from pokemons.querysets import PokemonQuerySet


class Type(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ability(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    is_main_series = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "abilities"

    def __str__(self):
        return self.name


class Pokemon(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    front_sprite = models.URLField(blank=True, null=True)
    types = models.ManyToManyField(
        Type,
        through="PokemonType",
        related_name="pokemons",
    )
    abilities = models.ManyToManyField(
        Ability,
        through="PokemonAbility",
        related_name="pokemons",
    )

    objects = PokemonQuerySet.as_manager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PokemonAbility(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    slot = models.IntegerField()
    is_hidden = models.BooleanField(default=False)

    class Meta:
        unique_together = [
            ("pokemon", "ability"),
            ("pokemon", "slot"),
        ]

    def __str__(self):
        return f"{self.pokemon.name} - {self.ability.name} slot: {self.slot}"


class PokemonType(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    slot = models.IntegerField()

    class Meta:
        unique_together = [
            ("pokemon", "type"),
            ("pokemon", "slot"),
        ]

    def __str__(self):
        return f"{self.pokemon.name} - {self.type.name} slot: {self.slot}"
