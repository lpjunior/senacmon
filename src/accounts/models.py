from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    display_name = models.CharField(max_length=100, blank=True)
    berries_cache = models.PositiveIntegerField(default=0)
    # será preenchido após escolher o starter, FK adiada para evitar import circular
    starter_pokemon_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'accounts_profile'

    def __str__(self):
        return self.display_name or self.user.username