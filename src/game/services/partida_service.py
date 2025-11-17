from django.db import transaction
from django.utils import timezone

from common.utils.rng import seed_rodada, sorteio_dado
from game.choices import EstadoPartida, TipoZona, ResultadoBatalha
from game.domain.validadores import garantir_nao_capturado
from game.models import Mapa, Partida, EventoRodada, Batalha
from wallet.services import saldo_atual
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
            mensagem_usuario=f"🚫 Capturado pela Equipe Rocket! Faltam {partida.rounds_restantes_captura} rodadas para se libertar",
            payload={"rounds_restantes": partida.rounds_restantes_captura},
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
        mensagem_usuario=f"🎲 Rolou {dado}! Moveu da posição {posix_antiga} → {posix_nova}",
        payload=payload_mov,
        criado_em=timezone.now()
    )

    payload_zona = aplicar_zona(partida, partida.rodada_atual, zona, valor)

    if zona != TipoZona.BATALHA:
        partida.rodada_atual += 1
        partida.save(update_fields=["rodada_atual", "atualizado_em"])

    # Verificar se atingiu o limite de rodadas e encerrar automaticamente
    if partida.rodada_atual > partida.rodada_limite:
        encerrar_partida(partida, "rodada_limite")
    
    # Verificar se saldo zerou e encerrar automaticamente
    saldo = saldo_atual(partida.user, partida)
    if saldo <= 0 and zona != TipoZona.BATALHA:
        encerrar_partida(partida, "saldo_zerado")

    return {
        "dado": dado,
        "posix_antiga": posix_antiga,
        "posix_nova": posix_nova,
        "zona": zona,
        "zona_payload": payload_zona
    }

@transaction.atomic
def gerar_resumo_final(partida: Partida) -> dict:
    """Gera resumo final da partida com estatísticas"""
    saldo_final = saldo_atual(partida.user, partida)
    
    # Contar batalhas
    batalhas = Batalha.objects.filter(partida=partida)
    total_batalhas = batalhas.count()
    vitorias = batalhas.filter(resultado=ResultadoBatalha.VITORIA).count()
    derrotas = batalhas.filter(resultado=ResultadoBatalha.DERROTA).count()
    sem_aposta = batalhas.filter(resultado=ResultadoBatalha.SEM_APOSTA).count()
    
    # Calcular ganhos/perdas
    from wallet.models import Transacao
    transacoes = Transacao.objects.filter(partida=partida)
    total_ganho = sum(t.valor for t in transacoes if t.valor > 0)
    total_perdido = abs(sum(t.valor for t in transacoes if t.valor < 0))
    
    resumo = {
        "rodadas_jogadas": partida.rodada_atual - 1,
        "posicao_final": partida.posicao_atual,
        "saldo_inicial": partida.berries_iniciais,
        "saldo_final": saldo_final,
        "lucro_liquido": saldo_final - partida.berries_iniciais,
        "total_batalhas": total_batalhas,
        "vitorias": vitorias,
        "derrotas": derrotas,
        "batalhas_sem_aposta": sem_aposta,
        "total_ganho": total_ganho,
        "total_perdido": total_perdido,
        "pokemon_usado": partida.pokemon_inicial.nome,
    }
    
    return resumo

@transaction.atomic
def encerrar_partida(partida: Partida, motivo: str):
    """Encerra uma partida e gera resumo final"""
    if partida.estado == EstadoPartida.ENCERRADA:
        return
    
    resumo = gerar_resumo_final(partida)
    resumo["motivo_encerramento"] = motivo
    
    partida.estado = EstadoPartida.ENCERRADA
    partida.resumo_final = resumo
    partida.save(update_fields=["estado", "resumo_final", "atualizado_em"])
    
    mensagens_motivo = {
        "rodada_limite": "Partida encerrada - limite de rodadas atingido",
        "saldo_zerado": "Partida encerrada - berries esgotadas",
        "abandono": "Partida encerrada - abandonada pelo jogador"
    }
    
    EventoRodada.objects.create(
        partida=partida,
        rodada=partida.rodada_atual,
        tipo_evento="fim",
        mensagem_usuario=mensagens_motivo.get(motivo, "Partida encerrada"),
        payload={"motivo": motivo, "resumo": resumo},
        criado_em=timezone.now()
    )