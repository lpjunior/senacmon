from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from game.models import Partida
from game.services.partida_service import consume_capture_cooldown, rolar_dados_e_resolver_zona
from game.domain.excecoes import ErroBloqueioCaptura

@login_required
def roll_view(request):
    if request.method != "POST":
        messages.error(request, "Ação inválida.")
        return redirect("game:state")

    partida = Partida.objects.filter(user=request.user, estado="em_andamento").first()
    if not partida:
        messages.info(request, "Nenhuma partida ativa.")
        return redirect("game:start")

    # Caso capturado, apenas consome rodada
    if consume_capture_cooldown(partida):
        messages.warning(request, "Você perdeu a rodada por estar capturado!")
        return redirect("game:state")

    try:
        result = rolar_dados_e_resolver_zona(partida)
    except ErroBloqueioCaptura:
        messages.warning(request, "Você ainda está capturado.")
        return redirect("game:state")

    zona = result["zona"]
    if zona == "batalha":
        messages.info(request, "Você entrou em uma batalha!")
        return redirect("game:battle")
    elif zona == "bonus":
        messages.success(request, "Você ganhou berries de bônus!")
    elif zona == "perda":
        messages.error(request, "Você perdeu algumas berries.")
    elif zona == "captura":
        messages.warning(request, "Equipe Rocket te capturou! Fique de fora por 2 rodadas.")
    else:
        messages.info(request, "Nada aconteceu nesta rodada.")

    return redirect("game:state")
