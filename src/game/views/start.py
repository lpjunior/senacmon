from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from game.models import Pokemon, Mapa, Partida
from game.services.partida_service import start_game


@login_required
def start_view(request):
    partida = Partida.objects.filter(user=request.user, estado="em_andamento").first()
    if partida:
        messages.info(request, "Você já possui uma partida em andamento.")
        return redirect("game:state")

    if request.method == "POST":
        starter_id = request.POST.get("pokemon_inicial")
        if not starter_id:
            messages.error(request, "Selecione um Pokémon para começar.")
            return redirect("game:start")

        try:
            starter = Pokemon.objects.get(id=starter_id, ativo=True)
        except Pokemon.DoesNotExist:
            messages.error(request, "Pokémon inválido.")
            return redirect("game:start")

        mapa = Mapa.objects.filter(ativo=True).first()
        if not mapa:
            messages.error(request, "Nenhum mapa ativo encontrado.")
            return redirect("game:start")

        partida = start_game(request.user, starter, mapa)
        messages.success(request, f"Partida iniciada com {starter.nome}!")
        return redirect("game:state")

    pokemons = Pokemon.objects.filter(ativo=True)
    return render(request, "game/start.html", {"pokemons": pokemons})
