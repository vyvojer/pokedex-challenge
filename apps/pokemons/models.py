from django.db import models

# Create your models here.


class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    types = models.ManyToManyField(
        Type,
        through="PokemonType",
        related_name="pokemons",
    )

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
