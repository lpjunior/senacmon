from django.conf import settings
from django.db import models

class Transacao(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transacoes", db_index=True)
    partida = models.ForeignKey("game.Partida", on_delete=models.CASCADE, related_name="transacoes", db_index=True)

    tipo = models.CharField(max_length=30)  # aposta_debito, aposta_credito, bonus, penalidade, ajuste
    valor = models.IntegerField()  # negativo debita, positivo credita
    saldo_resultante = models.IntegerField()

    referencia_tipo = models.CharField(max_length=30, blank=True)
    referencia_id = models.CharField(max_length=64, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wallet_transacao"
        indexes = [
            models.Index(fields=["user", "criado_em"], name="idx_tx_user_data"),
            models.Index(fields=["partida", "criado_em"], name="idx_tx_partida_data"),
            models.Index(fields=["tipo"], name="idx_tx_tipo"),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(saldo_resultante__gte=0), name="ck_tx_saldo_nao_neg"),
        ]

    def __str__(self):
        return f"{self.tipo} {self.valor} saldo {self.saldo_resultante}"
