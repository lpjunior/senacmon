from django.db import models

from game.choices import ResultadoBatalha
from game.models import Partida, Pokemon


class Batalha(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='batalhas', db_index=True)
    rodada = models.PositiveSmallIntegerField()

    pokemon_jogador = models.ForeignKey(Pokemon, on_delete=models.PROTECT, related_name='batalhas_como_jogador')
    pokemon_adversario = models.ForeignKey(Pokemon, on_delete=models.PROTECT, related_name='batalhas_como_adversario')

    escolhas_numeros = models.JSONField(default=list)
    houve_aposta = models.BooleanField(default=False)
    valor_aposta = models.PositiveIntegerField(default=0)

    numero_sorteado = models.PositiveSmallIntegerField(null=True, blank=True)
    resultado = models.CharField(max_length=15, choices=ResultadoBatalha.choices, null=True, blank=True)

    multiplicador_base = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    ajuste_elemental = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    multiplicador_efetivo = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)

    berries_delta = models.IntegerField(default=0)
    detalhe_elemental = models.JSONField(default=dict, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "game_batalha"
        indexes = [
            models.Index(fields=["partida", "rodada"], name="idx_batalha_partida_rodada"),
            models.Index(fields=["resultado"], name="idx_batalha_resultado"),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(valor_aposta__gte=0), name="ck_batalha_aposta_gte_0"),
            models.CheckConstraint(check=models.Q(multiplicador_efetivo__gte=1.00), name="ck_batalha_multi_min"),
        ]

    def __str__(self):
        return f"Batalha partida {self.partida.id} - rodada {self.rodada}"