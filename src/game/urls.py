"""Game URL configuration."""

from django.urls import path

from game.views import start, state, roll, battle

app_name = 'game'

urlpatterns = [
    path("start/", start.start_view, name="start"),
    path("state/", state.state_view, name="state"),
    path("roll/", roll.roll_view, name="roll"),
    path("battle/", battle.battle_view, name="battle"),
    path("battle/resolve/", battle.battle_resolve_view, name="battle_resolve"),
]