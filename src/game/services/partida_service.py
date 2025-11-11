from django.db import transaction
from django.utils import timezone

from common.utils.rng import seed_rodada, sorteio_dado
from game.choices import EstadoPartida, TipoZona
from game.domain.validadores import garantir_nao_capturado
from game.models import Mapa, Partida, EventoRodada
from game.services.mapa_service import avancar_posicao, obter_zona_da_posicao
from game.services.zona_service import aplicar_zona


@transaction.atomic
def start_game(user, starter_pokemon, mapa: Mapa, berries_iniciais: int = 100, rodada_limite: int = 10) -> Partida:
    partida = Partida.objects.create(
        user=user,
        mapa=mapa,
        estado=EstadoPartida.EM_ANDAMENTO,
        berries_iniciais=berries_iniciais,
        rodada_limite=rodada_limite,
        pokemon_inicial=starter_pokemon
    )

    EventoRodada.objects.create(
        partida=partida,
        rodada=1,
        tipo_evento="start",
        mensagem_usuario="Partida iniciada",
        payload={},
        criado_em=timezone.now()
    )
    return partida

@transaction.atomic
def consume_capture_cooldown(partida: Partida) -> bool:
    if partida.rounds_restantes_captura > 0:
        partida.rounds_restantes_captura -= 1
        partida.rodada_atual += 1
        partida.save(update_fields=["rounds_restantes_captura", "rodada_atual", "atualizado_em"])

        EventoRodada.objects.create(
            partida=partida,
            rodada=partida.rodada_atual - 1,
            tipo_evento="skip",
            mensagem_usuario="Você perdeu a vez por captura",
            payload={},
            criado_em=timezone.now()
        )
        return True
    return False

@transaction.atomic
def rolar_dados_e_resolver_zona(partida: Partida) -> dict:
    garantir_nao_capturado(partida.rounds_restantes_captura)

    seed = seed_rodada(partida.id, partida.rodada_atual)
    _, dado = sorteio_dado(seed)

    posix_antiga = partida.posicao_atual
    posix_nova = avancar_posicao(posix_antiga, dado, partida.mapa.tamanho_total)

    partida.posicao_atual = posix_nova
    partida.save(update_fields=["posicao_atual", "atualizado_em"])

    zona, valor = obter_zona_da_posicao(partida, posix_nova)

    payload_mov = {
        "seed": seed,
        "dado": dado,
        "posix_antiga": posix_antiga,
        "posix_nova": posix_nova,
        "zona": zona,
        "valor": valor,
    }

    EventoRodada.objects.create(
        partida=partida,
        rodada=partida.rodada_atual,
        tipo_evento="movimento",
        mensagem_usuario="Rolagem realizada",
        payload=payload_mov,
        criado_em=timezone.now()
    )

    payload_zona = aplicar_zona(partida, partida.rodada_atual, zona, valor)

    if zona != TipoZona.BATALHA:
        partida.rodada_atual += 1
        partida.save(update_fields=["rodada_atual", "atualizado_em"])

    return {
        "dado": dado,
        "posix_antiga": posix_antiga,
        "posix_nova": posix_nova,
        "zona": zona,
        "zona_payload": payload_zona
    }