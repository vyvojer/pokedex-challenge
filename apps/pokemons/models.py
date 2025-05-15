from django.db import models
from pokemons.querysets import PokemonQuerySet


class Type(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Pokemon(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    types = models.ManyToManyField(
        Type,
        through="PokemonType",
        related_name="pokemons",
    )

    objects = PokemonQuerySet.as_manager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


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
