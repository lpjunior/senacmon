from django.urls import path
from . import views
from .views import battle

app_name = "game"

urlpatterns = [
    path("start/", views.start_view, name="start"),   
    path("state/", views.state_view, name="state"),   
    path("roll/", views.roll_view, name="roll"),      
    path("battle/", views.battle_view, name="battle"),
    path("battle/resolve/", battle.battle_resolve_view, name="battle_resolve"),
    path("abandon/", views.abandon_view, name="abandon"),
]
