from django.test import TestCase
from django.urls import reverse

from factories.pokemons import PokemonFactory


class PokemonDetailViewTest(TestCase):
    def setUp(self):
        self.pokemon = PokemonFactory()

    def test_get(self):
        response = self.client.get(reverse("pokemons:pokemon_detail", kwargs={"pk": 1}))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.pokemon.name)


class ChangePageViewTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse("pokemons:change_page", kwargs={"page": 2}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, '<input id="page-input" type="hidden" name="page" value="2">'
        )
        self.assertEqual(response.headers.get("HX-Trigger-After-Swap"), "page-changed")


class ChangeOrderViewTest(TestCase):
    def test_get(self):
        response = self.client.get(
            reverse("pokemons:change_order", kwargs={"field": "name"}),
            data={"o": "id,name"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, '<input id="order-input" type="hidden" name="o" value="-name,id">'
        )
        self.assertEqual(response.headers.get("HX-Trigger-After-Swap"), "page-changed")
