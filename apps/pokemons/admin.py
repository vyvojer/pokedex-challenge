from django.contrib import admin

from .models import Pokemon, Type

# Register your models here.


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    filter_horizontal = ["types"]
    list_select_related = ["types"]

    autocomplete_fields = ["types"]
