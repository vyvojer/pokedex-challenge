from django.contrib import admin

from .models import Ability, Pokemon, PokemonAbility, PokemonType, Type

# Register your models here.


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    list_filter = ["is_main_series"]


class PokemonTypeInline(admin.TabularInline):
    model = PokemonType
    extra = 0
    can_delete = False
    readonly_fields = ["type", "slot"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PokemonAbilityInline(admin.TabularInline):
    model = PokemonAbility
    extra = 0
    can_delete = False
    verbose_name_plural = "Abilities"
    readonly_fields = ["ability", "slot", "is_hidden"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    list_select_related = True

    inlines = [PokemonTypeInline, PokemonAbilityInline]
