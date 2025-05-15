from django.urls import reverse
from pokemons.models import PokemonType
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factories.pokemons import PokemonFactory, TypeFactory


class TypeListAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("pokemons_api:type-list")

        self.type1 = TypeFactory(name="Fire")
        self.type2 = TypeFactory(name="Water")
        self.type3 = TypeFactory(name="Grass")

    def test_get_all_types(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        type_names = [t["name"] for t in response.data["results"]]
        self.assertIn("Fire", type_names)
        self.assertIn("Water", type_names)
        self.assertIn("Grass", type_names)


class TypeDetailAPIViewTest(APITestCase):
    def setUp(self):
        self.type = TypeFactory(name="Electric")
        self.url = reverse("pokemons_api:type-detail", kwargs={"pk": self.type.pk})

    def test_get_valid_type(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Electric")

    def test_get_invalid_type(self):
        invalid_url = reverse("pokemons_api:type-detail", kwargs={"pk": 999})
        response = self.client.get(invalid_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PokemonListViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("pokemons_api:pokemon-list")

        self.fire_type = TypeFactory(name="Fire")
        self.water_type = TypeFactory(name="Water")

        self.pokemon1 = PokemonFactory(name="Charmander")
        self.pokemon2 = PokemonFactory(name="Squirtle")

        PokemonType.objects.create(pokemon=self.pokemon1, type=self.fire_type, slot=1)
        PokemonType.objects.create(pokemon=self.pokemon2, type=self.water_type, slot=1)

    def test_get_all_pokemons(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pokemon_data = {p["name"]: p for p in response.data["results"]}

        self.assertIn("Charmander", pokemon_data)
        self.assertIn("Squirtle", pokemon_data)

        charmander = pokemon_data["Charmander"]
        charmander_type_names = [t["name"] for t in charmander["types"]]
        self.assertIn("Fire", charmander_type_names)

        squirtle = pokemon_data["Squirtle"]
        squirtle_type_names = [t["name"] for t in squirtle["types"]]
        self.assertIn("Water", squirtle_type_names)


class PokemonDetailViewTest(APITestCase):
    def setUp(self):

        self.fire_type = TypeFactory(name="Fire")
        self.flying_type = TypeFactory(name="Flying")

        self.pokemon = PokemonFactory(name="Charizard")

        PokemonType.objects.create(pokemon=self.pokemon, type=self.fire_type, slot=1)
        PokemonType.objects.create(pokemon=self.pokemon, type=self.flying_type, slot=2)

        self.url = reverse(
            "pokemons_api:pokemon-detail", kwargs={"pk": self.pokemon.pk}
        )

    def test_get_valid_pokemon(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Charizard")
        self.assertEqual(len(response.data["types"]), 2)

        type_names = [t["name"] for t in response.data["types"]]
        self.assertIn("Fire", type_names)
        self.assertIn("Flying", type_names)

    def test_get_invalid_pokemon(self):
        invalid_url = reverse("pokemons_api:pokemon-detail", kwargs={"pk": 999})
        response = self.client.get(invalid_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
