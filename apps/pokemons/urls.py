from django.urls import path

from . import views

app_name = "pokemons"

urlpatterns = [
    path("", views.PokemonListView.as_view(), name="pokemon_list"),
    path("<int:pk>/", views.PokemonDetailView.as_view(), name="pokemon_detail"),
    path("change-page/<int:page>/", views.change_page, name="change_page"),
    path("change-order/<str:field>/", views.change_order, name="change_order"),
]
