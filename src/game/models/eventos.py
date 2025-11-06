from django.db import models
from game.models import Partida

class EventoRodada(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name="eventos", db_index=True)
    rodada = models.PositiveSmallIntegerField()
    tipo_evento = models.CharField(max_length=30)
    mensagem_usuario = models.CharField(max_length=240, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "game_evento_rodada"
        indexes = [
            models.Index(fields=["partida", "rodada"], name="idx_evento_partida_rodada"),
            models.Index(fields=["partida", "criado_em"], name="idx_evento_partida_created"),
        ]

    def __str__(self):
        return f"Evento Partida: {self.partida.id} Rodada {self.rodada} - {self.tipo_evento}"
