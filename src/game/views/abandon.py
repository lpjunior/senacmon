from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from game.models import Partida
from game.services.partida_service import encerrar_partida
from game.choices import EstadoPartida

@login_required
def abandon_view(request):
    """Abandona a partida atual"""
    if request.method != "POST":
        messages.error(request, "Ação inválida.")
        return redirect("game:state")
    
    partida = Partida.objects.filter(user=request.user, estado=EstadoPartida.EM_ANDAMENTO).first()
    if not partida:
        messages.info(request, "Nenhuma partida ativa.")
        return redirect("game:start")
    
    encerrar_partida(partida, "abandono")
    messages.success(request, "Partida abandonada com sucesso.")
    return redirect("game:state")
