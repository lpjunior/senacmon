from django.utils import timezone
from django.db import transaction
from decimal import Decimal
from common.utils.rng import seed_rodada, sorteio_numero
from game.choices import ResultadoBatalha
from game.domain.excecoes import ErroEstadoInvalido
from game.domain.regras import PoliticaMultiplicador, resultado_elemental, multiplicador_efetivo
from game.models import Batalha, EventoRodada


def previa_batalha(batalha: Batalha, politica: PoliticaMultiplicador) -> dict:
    return {
        "oponente_nome": batalha.pokemon_adversario.nome,
        "oponente_elemento": batalha.pokemon_adversario.elemento,
        "jogador_elemento": batalha.pokemon_jogador.elemento,
        "min_simples": 5,
        "min_dupla": 8,
        "base_simples": politica.base_simples,
        "base_dupla": politica.base_dupla
    }

@transaction.atomic
def resolver_batalha(batalha: Batalha, numeros: list[int], valor_aposta: int | None, modo_simulacao: bool, politica: PoliticaMultiplicador) -> Batalha:
    if batalha.numero_sorteado is not None:
        raise ErroEstadoInvalido("Batalha já resolvida.")

    batalha.escolhas_numeros = numeros
    batalha.houve_aposta = bool(valor_aposta) and not modo_simulacao
    batalha.valor_aposta = int(valor_aposta or 0)

    seed = seed_rodada(batalha.partida.id, batalha.rodada)
    sorteado = sorteio_numero(seed, 0, 9)
    batalha.numero_sorteado = sorteado

    resultado = resultado_elemental(batalha.pokemon_jogador.elemento, batalha.pokemon_adversario.elemento)
    quantidade = len(numeros)
    mult_efetiva = multiplicador_efetivo(quantidade, resultado, politica)

    batalha.multiplicador_base = Decimal(politica.base_simples if quantidade == 1 else politica.base_dupla)
    batalha.ajuste_elemental = Decimal(mult_efetiva) - batalha.multiplicador_base
    batalha.multiplicador_efetivo = Decimal(mult_efetiva)

    venceu = sorteado in numeros
    if not batalha.houve_aposta:
        batalha.resultado = ResultadoBatalha.SEM_APOSTA
        batalha.berries_delta = 0
    else:
        if venceu:
            ganho = int(round(batalha.valor_aposta * float(mult_efetiva)))
            batalha.resultado = ResultadoBatalha.VITORIA
            batalha.berries_delta = ganho
        else:
            batalha.resultado = ResultadoBatalha.DERROTA
            batalha.berries_delta = -batalha.valor_aposta

    batalha.detalhe_elemental = {"resultado": resultado}
    batalha.save()

    EventoRodada.objects.create(
        partida=batalha.partida,
        rodada=batalha.rodada,
        tipo_evento="batalha",
        mensagem_usuario="Batalha resolvida",
        payload={
            "numeros": numeros,
            "sorteado": sorteado,
            "resultado": resultado,
            "houve_aposta": batalha.houve_aposta,
            "valor_aposta": batalha.valor_aposta,
            "resultado_batalha": batalha.resultado,
            "berries_delta": batalha.berries_delta,

        },
        criado_em=timezone.now()
    )

    partida = batalha.partida
    partida.rodada_atual += 1
    partida.save(update_fields=["rodada_atual", "atualizado_em"])

    return batalha