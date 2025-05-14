from django.urls import path
from pokemons import views_api

app_name = "pokemons_api"

urlpatterns = [
    path("types/", views_api.TypeListAPIView.as_view(), name="type-list"),
    path("types/<int:pk>/", views_api.TypeDetailAPIView.as_view(), name="type-detail"),
    path("pokemons/", views_api.PokemonListView.as_view(), name="pokemon-list"),
    path(
        "pokemons/<int:pk>/",
        views_api.PokemonDetailView.as_view(),
        name="pokemon-detail",
    ),
]
