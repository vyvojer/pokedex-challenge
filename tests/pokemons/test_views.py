from django.test import TestCase
from django.urls import reverse

from tests.factories.pokemons import AbilityFactory, PokemonFactory, TypeFactory


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


class AbilityDetailViewTest(TestCase):
    def setUp(self):
        self.ability = AbilityFactory()

    def test_get(self):
        response = self.client.get(
            reverse("pokemons:ability_detail", kwargs={"pk": self.ability.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ability.name)


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


class TypeListViewTest(TestCase):
    def setUp(self):
        self.type1 = TypeFactory(name="Normal")
        self.type2 = TypeFactory(name="Fire")
        self.type3 = TypeFactory(name="Water")

    def test_get__returns_full_page_with_entity_names(self):
        response = self.client.get(reverse("pokemons:type_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.type1.name)
        self.assertContains(response, self.type2.name)
        self.assertContains(response, self.type3.name)

        self.assertContains(response, "<body>")

    def test_get__with_htmx_header__returns_only_list_with_entity_names(self):
        response = self.client.get(
            reverse("pokemons:type_list"), headers={"HX-Request": "true"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.type1.name)
        self.assertContains(response, self.type2.name)
        self.assertContains(response, self.type3.name)

        self.assertNotContains(response, "<body>")

    def test_get__with_filter__returns_only_filtered_entities(self):
        response = self.client.get(
            reverse("pokemons:type_list"), data={"name__icontains": "orm"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.type1.name)
        self.assertNotContains(response, self.type2.name)
        self.assertNotContains(response, self.type3.name)


class AbilityListViewTest(TestCase):
    def setUp(self):
        self.ability1 = AbilityFactory(name="Overgrow")
        self.ability2 = AbilityFactory(name="Blaze")
        self.ability3 = AbilityFactory(name="Torrent")

    def test_get__returns_full_page_with_entity_names(self):
        response = self.client.get(reverse("pokemons:ability_list"))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.ability1.name)
        self.assertContains(response, self.ability2.name)
        self.assertContains(response, self.ability3.name)

        self.assertContains(response, "<body>")

    def test_get__with_htmx_header__returns_only_list_with_entity_names(self):
        response = self.client.get(
            reverse("pokemons:ability_list"), headers={"HX-Request": "true"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.ability1.name)
        self.assertContains(response, self.ability2.name)
        self.assertContains(response, self.ability3.name)

        self.assertNotContains(response, "<body>")

    def test_get__with_filter__returns_only_filtered_entities(self):
        response = self.client.get(
            reverse("pokemons:ability_list"), data={"name__icontains": "r"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.ability1.name)
        self.assertNotContains(response, self.ability2.name)
        self.assertContains(response, self.ability3.name)


class PokemonListViewTest(TestCase):
    def setUp(self):
        self.pokemon1 = PokemonFactory(name="Pikachu")
        self.pokemon2 = PokemonFactory(name="Charmander")
        self.pokemon3 = PokemonFactory(name="Squirtle")

    def test_get__returns_full_page_with_entity_names(self):
        response = self.client.get(reverse("pokemons:pokemon_list"))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.pokemon1.name)
        self.assertContains(response, self.pokemon2.name)
        self.assertContains(response, self.pokemon3.name)

        self.assertContains(response, "<body>")

    def test_get__with_htmx_header__returns_only_list_with_entity_names(self):
        response = self.client.get(
            reverse("pokemons:pokemon_list"), headers={"HX-Request": "true"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.pokemon1.name)
        self.assertContains(response, self.pokemon2.name)
        self.assertContains(response, self.pokemon3.name)

        self.assertNotContains(response, "<body>")

    def test_get__with_filter__returns_only_filtered_entities(self):
        response = self.client.get(
            reverse("pokemons:pokemon_list"), data={"name__icontains": "a"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.pokemon1.name)
        self.assertContains(response, self.pokemon2.name)
        self.assertNotContains(response, self.pokemon3.name)
