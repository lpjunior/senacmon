from django.contrib import admin
from ..models.batalha import Batalha

@admin.register(Batalha)
class BatalhaAdmin(admin.ModelAdmin):
    list_display = ("id", "partida", "rodada", "resultado", "valor_aposta", "multiplicador_efetivo", "berries_delta", "criado_em")
    list_filter = ("resultado", "criado_em")
    search_fields = ("partida__user__username",)
    readonly_fields = ("numero_sorteado", "multiplicador_efetivo", "berries_delta")
