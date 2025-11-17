from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def start_view(request):
    return render(request, "game/start.html")


@login_required
def start_confirm_view(request):
    if request.method == "POST":
        return redirect("game:state")
    return redirect("game:start")


@login_required
def state_view(request):
    return render(request, "game/board.html")


@login_required
def board_view(request):
    return render(request, "game/board.html")


@login_required
def battle_view(request):
    return render(request, "game/battle.html")
