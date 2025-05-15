from django.test import TestCase
from django.urls import reverse

from tests.factories.pokemons import PokemonFactory, TypeFactory


class PokemonDetailViewTest(TestCase):
    def setUp(self):
        self.pokemon = PokemonFactory()

    def test_get(self):
        response = self.client.get(
            reverse("pokemons:pokemon_detail", kwargs={"pk": self.pokemon.id})
        )

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


class TypeDetailViewTest(TestCase):
    def setUp(self):
        self.type = TypeFactory()

    def test_get(self):
        response = self.client.get(
            reverse("pokemons:type_detail", kwargs={"pk": self.type.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.type.name)


class ComparisonViewTest(TestCase):
    def setUp(self):
        self.pokemon_1 = PokemonFactory(name="Pikachu")
        self.pokemon_2 = PokemonFactory(name="Charmander")
        self.pokemon_3 = PokemonFactory(name="Squirtle")

        session = self.client.session
        session["pokemon_comparison_ids"] = [self.pokemon_1.id, self.pokemon_3.id]
        session.save()

    def test_get__returns_full_page(self):

        response = self.client.get(reverse("pokemons:comparison"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pikachu")
        self.assertContains(response, "Squirtle")
        self.assertNotContains(response, "Charmander")

        self.assertContains(response, "<body>")

    def test_get_htmx__returns_only_part_of_page(self):

        response = self.client.get(
            reverse("pokemons:comparison"), headers={"HX-Request": "true"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pikachu")
        self.assertContains(response, "Squirtle")
        self.assertNotContains(response, "Charmander")

        self.assertNotContains(response, "<body>")


class ComparisonPokemonListViewTest(TestCase):
    def setUp(self):
        self.pokemon_1 = PokemonFactory(name="Pikachu")
        self.pokemon_2 = PokemonFactory(name="Charmander")
        self.pokemon_3 = PokemonFactory(name="Squirtle")

    def test_get__returns_filtered_pokemon_list(self):
        response = self.client.get(
            reverse("pokemons:comparison_pokemon_list"), data={"name__icontains": "e"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, "Pikachu")
        self.assertContains(response, "Charmander")
        self.assertContains(response, "Squirtle")


class ComparisonAddPokemonViewTest(TestCase):
    def setUp(self):
        session = self.client.session
        session["pokemon_comparison_ids"] = [1, 2]
        session.save()

    def test_get__add_pokemon_to_comparison(self):
        response = self.client.get(
            reverse("pokemons:comparison_add_pokemon", kwargs={"pk": 3})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session["pokemon_comparison_ids"], [1, 2, 3])
        self.assertEqual(response.headers.get("HX-Trigger"), "pokemon-added-or-removed")
