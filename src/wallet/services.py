from django.db import transaction
from wallet.models import Transacao

def saldo_atual(user, partida) -> int:
    ultima_transacao = Transacao.objects.filter(user=user, partida=partida).order_by("-id").first()
    return ultima_transacao.saldo_resultante if ultima_transacao else partida.berries_iniciais

@transaction.atomic
def debitar(user, partida, valor: int, ref_tipo: str, ref_id: str):
    atual = saldo_atual(user, partida)
    novo = max(atual - valor, 0)
    Transacao.objects.create(
        user=user,
        partida=partida,
        tipo="aposta_debito",
        valor=-valor,
        saldo_resultante=novo,
        referencia_tipo=ref_tipo,
        referencia_id=ref_id,
    )
    return novo

@transaction.atomic
def creditar(user, partida, valor: int, ref_tipo: str, ref_id: str):
    atual = saldo_atual(user, partida)
    novo = atual + valor
    Transacao.objects.create(
        user=user,
        partida=partida,
        tipo="aposta_credito",
        valor=valor,
        saldo_resultante=novo,
        referencia_tipo=ref_tipo,
        referencia_id=ref_id,
    )
    return novo