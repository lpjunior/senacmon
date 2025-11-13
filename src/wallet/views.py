from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Transacao
from game.models import Partida
from .services import saldo_atual

@login_required
def balance_view(request):
    partida = Partida.objects.filter(user=request.user, estado="em_andamento").first()
    saldo = saldo_atual(request.user, partida) if partida else 0
    return render(request, "wallet/balance.html", {"saldo": saldo})

@login_required
def transactions_view(request):
    transacoes = Transacao.objects.filter(user=request.user).order_by("-id")[:20]
    return render(request, "wallet/transactions.html", {"transacoes": transacoes})
