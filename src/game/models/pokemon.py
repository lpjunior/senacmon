from django.db import models
from ..choices import Elemento

class Pokemon(models.Model):
    nome = models.CharField(max_length=40, unique=True)
    elemento = models.CharField(max_length=10, choices=Elemento.choices, db_index=True)
    numero_associado = models.PositiveIntegerField(unique=True)
    sprite_url = models.URLField(blank=True)
    ativo = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = "game_pokemon"
        indexes = [models.Index(fields=["elemento", "ativo"], name="idx_pokemon_elem_ativo")]

    def __str__(self):
        return f"{self.nome} ({self.elemento})"