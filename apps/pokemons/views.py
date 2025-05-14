from django.shortcuts import render
from django.views.generic import ListView
from django_filters.views import FilterView
from pokemons.filters import PokemonFilter
from pokemons.models import Pokemon


class PokemonListView(FilterView, ListView):
    """
    HTMX-based list view for Pokemon model with filtering and pagination.
    """

    model = Pokemon
    queryset = Pokemon.objects.prefetched()
    template_name = "pokemons/pokemons.html"
    context_object_name = "pokemons"
    paginate_by = 30
    filterset_class = PokemonFilter

    def get_template_names(self):
        """
        Return different template names based on whether the request is an HTMX request.
        """
        if self.request.headers.get("HX-Request"):
            return ["pokemons/pokemon_list.html"]
        return [self.template_name]
