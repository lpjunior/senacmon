from django.contrib import admin
from game.models import Pokemon


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('nome', 'elemento', 'numero_associado', 'ativo')
    search_filter = ('elemento', 'ativo')
    search_fields = ('nome',)