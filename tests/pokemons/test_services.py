from django.test import SimpleTestCase
from pokemons.services import change_filter_ordering


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
