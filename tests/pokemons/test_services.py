from django.test import RequestFactory, SimpleTestCase, TestCase
from pokemons.services import PokemonComparisonInformation, change_filter_ordering

from tests.factories.pokemons import PokemonFactory


class ChangeFilterOrderingsTestCase(SimpleTestCase):
    def test_change_filter_ordering__empty_ordering__returns_field(self):
        field_name = "some_field"
        ordering_value = None
        ordering = change_filter_ordering(ordering=ordering_value, field=field_name)
        self.assertEqual(ordering, "some_field")

    def test_change_filter_ordering__field_not_in_ordering__add_field_at_the_beginning(
        self,
    ):
        field_name = "some_field"
        ordering_value = "-field_1,field_2"
        ordering = change_filter_ordering(ordering=ordering_value, field=field_name)
        self.assertEqual(ordering, "some_field,-field_1,field_2")

    def test_change_filter_ordering__ascending_field_in_ordering__add_descending_field_at_the_beginning(
        self,
    ):
        field_name = "some_field"
        ordering_value = "-field_1,some_field,field_2"
        ordering = change_filter_ordering(ordering=ordering_value, field=field_name)
        self.assertEqual(ordering, "-some_field,-field_1,field_2")

    def test_change_filter_ordering__descending_field_in_ordering__add_asscending_field_at_the_beginning(
        self,
    ):
        field_name = "some_field"
        ordering_value = "-field_1,field_2,-some_field"
        ordering = change_filter_ordering(ordering=ordering_value, field=field_name)
        self.assertEqual(ordering, "some_field,-field_1,field_2")


class PokemonComparisonInformationTestCase(TestCase):
    def setUp(self):
        factory = RequestFactory()
        self.request = factory.get("/")
        self.request.session = {}
        self.comparison_info = PokemonComparisonInformation(
            request=self.request, max_number=3
        )
        self.pokemon_1 = PokemonFactory(id=1)
        self.pokemon_2 = PokemonFactory(id=2)
        self.pokemon_3 = PokemonFactory(id=3)

    def test_init(self):
        self.assertEqual(self.comparison_info.max_number, 3)
        self.assertEqual(self.comparison_info.pokemon_ids, [])
        self.assertEqual(
            self.request.session.get(PokemonComparisonInformation.SESSION_KEY), []
        )

    def test_add_pokemon__adds_pokemon(self):
        self.comparison_info.add_pokemon(1)
        self.assertEqual(self.comparison_info.pokemon_ids, [1])
        self.assertEqual(
            self.request.session.get(PokemonComparisonInformation.SESSION_KEY), [1]
        )

        self.comparison_info.add_pokemon(2)
        self.assertEqual(self.comparison_info.pokemon_ids, [1, 2])
        self.assertEqual(
            self.request.session.get(PokemonComparisonInformation.SESSION_KEY), [1, 2]
        )

        # Try to add a duplicate pokemon
        self.comparison_info.add_pokemon(1)
        self.assertEqual(self.comparison_info.pokemon_ids, [1, 2])
        self.assertEqual(
            self.request.session.get(PokemonComparisonInformation.SESSION_KEY), [1, 2]
        )

    def test_add_pokemon__full__does_not_add(self):
        self.comparison_info.add_pokemon(1)
        self.comparison_info.add_pokemon(2)
        self.comparison_info.add_pokemon(3)
        self.comparison_info.add_pokemon(4)
        self.assertEqual(self.comparison_info.pokemon_ids, [1, 2, 3])
        self.assertEqual(
            self.request.session.get(PokemonComparisonInformation.SESSION_KEY),
            [1, 2, 3],
        )

    def test_remove_pokemon__removes_pokemon(self):
        self.comparison_info.add_pokemon(1)
        self.comparison_info.add_pokemon(2)

        self.comparison_info.remove_pokemon(1)
        self.assertEqual(self.comparison_info.pokemon_ids, [2])
        self.assertEqual(
            self.request.session.get(PokemonComparisonInformation.SESSION_KEY), [2]
        )

        # Try to remove a non-existent pokemon

        self.comparison_info.remove_pokemon(3)
        self.assertEqual(self.comparison_info.pokemon_ids, [2])
        self.assertEqual(
            self.request.session.get(PokemonComparisonInformation.SESSION_KEY), [2]
        )

    def test_get_pokemons__returns_pokemons(self):
        self.comparison_info.add_pokemon(1)
        self.comparison_info.add_pokemon(2)

        pokemons = self.comparison_info.get_pokemons()

        self.assertQuerySetEqual(
            pokemons,
            [
                self.pokemon_1,
                self.pokemon_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    def test_is_full__returns_true_when_is_full(self):
        self.comparison_info.add_pokemon(1)
        self.comparison_info.add_pokemon(2)
        self.assertFalse(self.comparison_info.is_full())

        self.comparison_info.add_pokemon(3)
        self.assertTrue(self.comparison_info.is_full())
