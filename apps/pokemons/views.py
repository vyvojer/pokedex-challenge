from django.conf import settings
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django_filters.views import FilterView
from pokemons import services
from pokemons.filters import PokemonFilter, TypeFilter
from pokemons.models import Pokemon, Type


class PokemonListView(FilterView, ListView):
    """
    HTMX-based list view for Pokemon model with filtering and pagination.
    """

    model = Pokemon
    queryset = Pokemon.objects.prefetched()
    template_name = "pokemons/pokemons.html"
    context_object_name = "pokemons"
    paginate_by = settings.PAGE_SIZE
    filterset_class = PokemonFilter

    def get_template_names(self):
        """
        Return different template names based on whether the request is an HTMX request.
        """
        if self.request.headers.get("HX-Request"):
            return ["pokemons/pokemon_list.html"]
        return [self.template_name]


class PokemonDetailView(DetailView):
    model = Pokemon
    template_name = "pokemons/pokemon_detail.html"


def change_page(request, page: int) -> HttpResponse:
    html = f'<input id="page-input" type="hidden" name="page" value="{page}">'
    # We set the HX-Trigger-After-Swap header to trigger list reload after "page-input" has been swapped.
    # See the form "hx-trigger"
    return HttpResponse(html, headers={"HX-Trigger-After-Swap": "page-changed"})


def change_order(request, field: str) -> HttpResponse:
    o = request.GET.get("o", None)
    ordering = services.change_filter_ordering(ordering=o, field=field)
    html = f'<input id="order-input" type="hidden" name="o" value="{ordering}">'
    return HttpResponse(html, headers={"HX-Trigger-After-Swap": "page-changed"})


class TypeListView(FilterView, ListView):
    """
    HTMX-based list view for Type model with filtering and pagination.
    """

    model = Type
    queryset = Type.objects.all()
    template_name = "pokemons/types.html"
    context_object_name = "types"
    paginate_by = settings.PAGE_SIZE
    filterset_class = TypeFilter

    def get_template_names(self):
        """
        Return different template names based on whether the request is an HTMX request.
        """
        if self.request.headers.get("HX-Request"):
            return ["pokemons/type_list.html"]
        return [self.template_name]


class TypeDetailView(DetailView):
    model = Type
    template_name = "pokemons/type_detail.html"
