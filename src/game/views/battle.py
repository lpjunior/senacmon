from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from game.domain.excecoes import ErroDominio
from game.domain.regras import PoliticaMultiplicador
from game.models import Partida, Batalha
from game.services.aposta_service import preparar_e_cobrar_aposta, pagar_premio
from game.services.batalha_service import previa_batalha, resolver_batalha
from wallet.services import saldo_atual

@login_required
def battle_view(request):
    partida = Partida.objects.filter(user=request.user, estado="em_andamento").first()
    if not partida:
        messages.error(request, "Nenhuma partida ativa.")
        return redirect("game:start")

    batalha = Batalha.objects.filter(partida=partida, rodada=partida.rodada_atual, numero_sorteado__isnull=True).first()
    if not batalha:
        messages.info(request, "Nenhuma batalha pendente.")
        return redirect("game:state")

    policy = PoliticaMultiplicador()
    preview = previa_batalha(batalha, policy)
    saldo = saldo_atual(request.user, partida)
    return render(request, "game/battle.html", {"batalha": batalha, "preview": preview, "saldo": saldo})

@login_required
def battle_resolve_view(request):
    if request.method != "POST":
        return redirect("game:state")

    partida = Partida.objects.filter(user=request.user, estado="em_andamento").first()
    if not partida:
        messages.error(request, "Nenhuma partida ativa.")
        return redirect("game:start")

    batalha = Batalha.objects.filter(partida=partida, rodada=partida.rodada_atual).first()
    if not batalha:
        messages.error(request, "Nenhuma batalha para resolver.")
        return redirect("game:state")


    raw_numeros = [n.strip() for n in request.POST.getlist("numeros") if n.strip() != '']

    if not raw_numeros:
        messages.error(request, "Informe pelo menos um número para a batalha.")
        return redirect("game:battle")

    numeros = [int(n) for n in raw_numeros]
    valor = request.POST.get("valor_aposta")
    valor_aposta = int(valor) if valor else 0
    modo_simulacao = request.POST.get("modo") == "simular"
    policy = PoliticaMultiplicador()

    try:
        if not modo_simulacao and valor_aposta > 0:
            preparar_e_cobrar_aposta(request.user, partida, numeros, valor_aposta, 5, 8, 20)
        batalha = resolver_batalha(batalha, numeros, valor_aposta, modo_simulacao, policy)
        if batalha.resultado == "vitoria" and batalha.houve_aposta:
            pagar_premio(request.user, partida, batalha.berries_delta)
        messages.success(request, f"Batalha resolvida: {batalha.get_resultado_display()}")
    except ErroDominio as e:
        messages.error(request, str(e))
        return redirect("game:battle")

    return redirect("game:state")
