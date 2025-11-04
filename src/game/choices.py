from django.db import models

class Elemento(models.TextChoices):
    AGUA = "agua", "Água"
    FOGO = "fogo", "Fogo"
    PLANTA = "planta", "Planta"

class TipoZona(models.TextChoices):
    NEUTRA = "neutra", "Neutra"
    BONUS = "bonus", "Bônus"
    PERDA = "perda", "Perda"
    BATALHA = "batalha", "Batalha"
    CAPTURA = "captura", "Captura"

class EstadoPartida(models.TextChoices):
    EM_ANDAMENTO = "em_andamento", "Em andamento"
    ENCERRADA = "encerrada", "Encerrada"

class ResultadoBatalha(models.TextChoices):
    VITORIA = "vitoria", "Vitoria"
    DERROTA = "derrota", "Derrota"
    SEM_APOSTA = "sem_aposta", "Sem aposta"