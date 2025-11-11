from django.contrib import admin
from wallet.models import Transacao

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "partida", "tipo", "saldo_resultante", "criado_em"]
    list_filter = ("tipo", "criado_em")
    search_fields = ("user__username", "referencia_id")
    readonly_fields = ("saldo_resultante",)