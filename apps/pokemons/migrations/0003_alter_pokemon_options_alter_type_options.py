# Generated by Django 5.2.1 on 2025-05-14 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pokemons", "0002_alter_pokemon_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="pokemon",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="type",
            options={"ordering": ["name"]},
        ),
    ]
