from django.test import TestCase
from pokemons.filters import AbilityFilter, PokemonFilter, TypeFilter
from pokemons.models import Ability, Pokemon, Type

from tests.factories.pokemons import AbilityFactory, PokemonFactory, TypeFactory


class TypeFilterTest(TestCase):
    def setUp(self):
        self.type_1 = TypeFactory(id=2, name="Normal")
        self.type_2 = TypeFactory(id=1, name="Fire")
        self.type_3 = TypeFactory(id=3, name="Water")

    def test_filter_by_name_icontains(self):
        filter_data = {"name__icontains": "or"}
        filterset = TypeFilter(filter_data, queryset=Type.objects.all())

        self.assertQuerySetEqual(
            filterset.qs, [self.type_1], transform=lambda x: x, ordered=False
        )

    def test_ordering(self):
        filter_data = {"o": "id"}
        filterset = TypeFilter(filter_data, queryset=Type.objects.all())

        self.assertQuerySetEqual(
            filterset.qs,
            [self.type_2, self.type_1, self.type_3],
            transform=lambda x: x,
            ordered=True,
        )

        filter_data = {"o": "-id"}
        filterset = TypeFilter(filter_data, queryset=Type.objects.all())

        self.assertQuerySetEqual(
            filterset.qs,
            [self.type_3, self.type_1, self.type_2],
            transform=lambda x: x,
            ordered=True,
        )


class AbilityFilterTest(TestCase):
    def setUp(self):
        self.type_1 = AbilityFactory(id=2, name="Overgrow")
        self.type_2 = AbilityFactory(id=1, name="Blaze")
        self.type_3 = AbilityFactory(id=3, name="Torrent")

    def test_filter_by_name_icontains(self):
        filter_data = {"name__icontains": "ver"}
        filterset = AbilityFilter(filter_data, queryset=Ability.objects.all())

        self.assertQuerySetEqual(
            filterset.qs, [self.type_1], transform=lambda x: x, ordered=False
        )

    def test_ordering(self):
        filter_data = {"o": "id"}
        filterset = AbilityFilter(filter_data, queryset=Ability.objects.all())

        self.assertQuerySetEqual(
            filterset.qs,
            [self.type_2, self.type_1, self.type_3],
            transform=lambda x: x,
            ordered=True,
        )

        filter_data = {"o": "-id"}
        filterset = AbilityFilter(filter_data, queryset=Ability.objects.all())

        self.assertQuerySetEqual(
            filterset.qs,
            [self.type_3, self.type_1, self.type_2],
            transform=lambda x: x,
            ordered=True,
        )


class PokemonFilterTest(TestCase):
    def setUp(self):
        self.type_1 = PokemonFactory(id=2, name="Pikachu")
        self.type_2 = PokemonFactory(id=1, name="Charmander")
        self.type_3 = PokemonFactory(id=3, name="Squirtle")

    def test_filter_by_name_icontains(self):
        filter_data = {"name__icontains": "kac"}
        filterset = PokemonFilter(filter_data, queryset=Pokemon.objects.all())

        self.assertQuerySetEqual(
            filterset.qs, [self.type_1], transform=lambda x: x, ordered=False
        )

    def test_ordering(self):
        filter_data = {"o": "id"}
        filterset = PokemonFilter(filter_data, queryset=Pokemon.objects.all())

        self.assertQuerySetEqual(
            filterset.qs,
            [self.type_2, self.type_1, self.type_3],
            transform=lambda x: x,
            ordered=True,
        )

        filter_data = {"o": "-id"}
        filterset = PokemonFilter(filter_data, queryset=Pokemon.objects.all())

        self.assertQuerySetEqual(
            filterset.qs,
            [self.type_3, self.type_1, self.type_2],
            transform=lambda x: x,
            ordered=True,
        )
