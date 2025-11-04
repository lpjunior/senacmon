from django.conf import settings
from django.db import models

from game.choices import EstadoPartida
from game.models.mapa import Mapa
from game.models.pokemon import Pokemon

class Partida(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="partidas")
    mapa = models.ForeignKey(Mapa, on_delete=models.PROTECT, related_name="partida")
    estado = models.CharField(max_length=20, choices=EstadoPartida.choices, default=EstadoPartida.EM_ANDAMENTO, db_index=True)

    berries_iniciais = models.PositiveIntegerField(default=100)
    rodada_limite = models.PositiveSmallIntegerField(default=10)

    rodada_atual = models.PositiveSmallIntegerField(default=1)
    posicao_atual = models.PositiveSmallIntegerField(default=1)
    rounds_restantes_captura = models.PositiveSmallIntegerField(default=0)

    pokemon_inicial = models.ForeignKey(Pokemon, on_delete=models.PROTECT, related_name="partidas_iniciadas")

    resumo_final = models.JSONField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "game_partida"
        indexes = [
            models.Index(fields=["user", "estado"], name="idx_partida_user_estado"),
            models.Index(fields=["atualizado_em"], name="idx_partida_update"),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(rodada_atual__gte=1), name="ck_rodadaatual_gte_1"),
            models.CheckConstraint(check=models.Q(posicao_atual__gte=1), name="ck_posicaoatual_gte_1"),
        ]

    def __str__(self):
        return f"Partida {self.id} de {self.user}"