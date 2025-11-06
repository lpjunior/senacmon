from django.contrib import admin
from ..models.partida import Partida

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "estado", "rodada_atual", "posicao_atual", "rounds_restantes_captura", "criado_em")
    list_filter = ("estado", "criado_em")
    search_fields = ("user__username",)
