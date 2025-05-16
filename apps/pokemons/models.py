from django.db import models
from pokemons.querysets import PokemonQuerySet


class Type(models.Model):
    """
    Model representing a Pokemon type.

    Types define the elemental properties of Pokemon and affect their strengths and weaknesses.

    Attributes:
        name: The name of the type (e.g., "Fire", "Water", "Electric").
    """

    name = models.CharField(max_length=100, db_index=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """
        Returns a string representation of the type.

        Returns:
            The name of the type.
        """
        return self.name


class Ability(models.Model):
    """
    Model representing a Pokemon ability.

    Attributes:
        name: The name of the ability.
        is_main_series: Whether the ability appears in the main series games.
    """

    name = models.CharField(max_length=100, db_index=True)
    is_main_series = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "abilities"

    def __str__(self):
        """
        Returns a string representation of the ability.

        Returns:
            The name of the ability.
        """
        return self.name


class Pokemon(models.Model):
    """
    Model representing a Pokemon.

    Attributes:
        name: The name of the Pokemon.
        weight: The weight of the Pokemon in hectograms.
        height: The height of the Pokemon in decimeters.
        front_sprite: URL to the front sprite image of the Pokemon.
        types: Many-to-many relationship with Type model through PokemonType.
        abilities: Many-to-many relationship with Ability model through PokemonAbility.
    """

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
        """
        Returns a string representation of the Pokemon.

        Returns:
            The name of the Pokemon.
        """
        return self.name


class PokemonAbility(models.Model):
    """
    Model representing the relationship between a Pokemon and an Ability.

    This is a through model for the many-to-many relationship between Pokemon and Ability.

    Attributes:
        pokemon: Foreign key to the Pokemon model.
        ability: Foreign key to the Ability model.
        slot: The slot number of the ability (1, 2, or 3).
        is_hidden: Whether the ability is a hidden ability.
    """

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
        """
        Returns a string representation of the Pokemon-Ability relationship.

        Returns:
            A string in the format "Pokemon name - Ability name slot: slot number".
        """
        return f"{self.pokemon.name} - {self.ability.name} slot: {self.slot}"


class PokemonType(models.Model):
    """
    Model representing the relationship between a Pokemon and a Type.

    This is a through model for the many-to-many relationship between Pokemon and Type.

    Attributes:
        pokemon: Foreign key to the Pokemon model.
        type: Foreign key to the Type model.
        slot: The slot number of the type (1 or 2).
    """

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    slot = models.IntegerField()

    class Meta:
        unique_together = [
            ("pokemon", "type"),
            ("pokemon", "slot"),
        ]

    def __str__(self):
        """
        Returns a string representation of the Pokemon-Type relationship.

        Returns:
            A string in the format "Pokemon name - Type name slot: slot number".
        """
        return f"{self.pokemon.name} - {self.type.name} slot: {self.slot}"
