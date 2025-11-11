from game.domain.excecoes import ErroSaldoInsuficiente
from game.domain.validadores import validar_aposta
from wallet.services import saldo_atual, debitar, creditar

def preparar_e_cobrar_aposta(usuario, partida, numeros: list[int], valor: int, minimo_simples: int, minimo_dupla: int, max_por_rodada: int):
    validar_aposta(numeros, valor, minimo_simples, minimo_dupla, max_por_rodada)
    saldo = saldo_atual(usuario, partida)

    if saldo < valor:
        raise ErroSaldoInsuficiente("Saldo insuficiente.")
    debitar(usuario, partida, valor, ref_tipo="batalha", ref_id=f"bet-{partida.id}-{partida.rodada_atual}")

def pagar_premio(usuario, partida, valor: int):
    if valor > 0:
        creditar(usuario, partida, valor, ref_tipo="batalha", ref_id=f"win-{partida.id}-{partida.rodada_atual}")