from django.urls import path

from . import views

app_name = 'pokemons'

urlpatterns = [
    path('', views.PokemonListView.as_view(), name='pokemon_list'),
]
