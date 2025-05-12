from django.contrib import admin

from .models import Pokemon, PokemonType, Type

# Register your models here.


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


class PokemonTypeInline(
    admin.TabularInline
):  # or admin.StackedInline for a different layout
    model = PokemonType
    extra = 0
    can_delete = False
    readonly_fields = ["type", "slot"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    list_select_related = True

    inlines = [PokemonTypeInline]
