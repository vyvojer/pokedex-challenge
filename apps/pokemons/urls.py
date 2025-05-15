from django.urls import path

from . import views

app_name = "pokemons"

urlpatterns = [
    path("", views.PokemonListView.as_view(), name="pokemon_list"),
    path("<int:pk>/", views.PokemonDetailView.as_view(), name="pokemon_detail"),
    path("types/", views.TypeListView.as_view(), name="type_list"),
    path("types/<int:pk>/", views.TypeDetailView.as_view(), name="type_detail"),
    path("abilities/", views.AbilityListView.as_view(), name="ability_list"),
    path(
        "abilities/<int:pk>/", views.AbilityDetailView.as_view(), name="ability_detail"
    ),
    path("change-page/<str:page>/", views.change_page, name="change_page"),
    path("change-order/<str:field>/", views.change_order, name="change_order"),
    path("comparison/", views.ComparisonView.as_view(), name="comparison"),
    path(
        "comparison/pokemon-list/",
        views.ComparisonPokemonListView.as_view(),
        name="comparison_pokemon_list",
    ),
    path(
        "comparison/add-pokemon/<int:pk>/",
        views.comparison_add_pokemon,
        name="comparison_add_pokemon",
    ),
    path(
        "comparison/remove-pokemon/<int:pk>/",
        views.comparison_remove_pokemon,
        name="comparison_remove_pokemon",
    ),
]
