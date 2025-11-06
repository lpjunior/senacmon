from django.db import models
from game.choices import TipoZona

class Mapa(models.Model):
    nome = models.CharField(max_length=100)
    tamanho_total = models.PositiveIntegerField()
    ativo = models.BooleanField(default=True)
    config_hash = models.CharField(max_length=64, blank=True)

    class Meta:
        db_table = "game_mapa"

    def __str__(self):
        return f"{self.nome} ({self.tamanho_total})"

class MapaPosicao(models.Model):
    mapa = models.ForeignKey(Mapa, on_delete=models.CASCADE, related_name="posicoes")
    posicao = models.PositiveIntegerField()
    tipo_zona = models.CharField(max_length=15, choices=TipoZona.choices)
    valor_param = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "game_mapa_posicao"
        verbose_name = "Mapa Posição"
        verbose_name_plural = "Mapa Posições"
        constraints = [
            models.UniqueConstraint(fields=["mapa", "posicao"], name="uq_mapa_posicao"),
            models.CheckConstraint(check=models.Q(posicao__gte=1), name="ck_posicao_gte_1"),
        ]
        indexes = [
            models.Index(fields=["mapa", "tipo_zona"], name="idx_mapa_tipozona"),
        ]

    def __str__(self):
        return f"{self.mapa.nome} ({self.tipo_zona})"