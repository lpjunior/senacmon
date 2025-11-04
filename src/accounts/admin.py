from django.contrib import admin
from accounts.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'berries_cache', 'starter_pokemon_id',)
    search_fields = ('user__username', 'display_name')
    readonly_fields = ()