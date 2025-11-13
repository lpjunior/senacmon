from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from wallet.services import saldo_atual
from game.models import Partida, EventoRodada, Batalha
from game.choices import EstadoPartida

@login_required
def state_view(request):
    partida = Partida.objects.filter(user=request.user, estado=EstadoPartida.EM_ANDAMENTO).first()
    if not partida:
        messages.info(request, "Nenhuma partida ativa. Comece uma nova!")
        return redirect("game:start")

    saldo = saldo_atual(request.user, partida)
    eventos = EventoRodada.objects.filter(partida=partida).order_by("-id")[:10]
    batalha_pendente = Batalha.objects.filter(partida=partida, rodada=partida.rodada_atual, numero_sorteado__isnull=True).first()

    context = {
        "partida": partida,
        "saldo": saldo,
        "eventos": eventos,
        "batalha_pendente": batalha_pendente,
    }
    return render(request, "game/board.html", context)
