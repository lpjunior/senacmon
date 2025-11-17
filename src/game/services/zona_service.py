from django.utils import timezone
from game.choices import TipoZona
from game.domain.excecoes import ErroBatalhaAtiva
from game.models import Partida, Batalha, Pokemon, EventoRodada
from wallet.services import creditar, debitar


def aplicar_zona(partida: Partida, rodada: int, zona: str, valor_param: int | None) -> dict:
    payload = {"zona": zona, "valor": valor_param}
    mensagem = ""

    if zona == TipoZona.BONUS:
        creditar(partida.user, partida, valor_param or 0, ref_tipo="sistema", ref_id=f"bonus-{rodada}")
        mensagem = f"💰 Zona de Bônus! +{valor_param} berries"

    elif zona == TipoZona.PERDA:
        if valor_param:
            debitar(partida.user, partida, abs(valor_param), ref_tipo="sistema", ref_id=f"perda-{rodada}")
            mensagem = f"💸 Zona de Perda! -{abs(valor_param)} berries"
        else:
            mensagem = "⚠️ Zona de Perda (sem valor)"

    elif zona == TipoZona.CAPTURA:
        partida.rounds_restantes_captura = 2
        partida.save(update_fields=["rounds_restantes_captura", "atualizado_em"])
        mensagem = "🚨 Capturado pela Equipe Rocket! Você ficará 2 rodadas sem jogar"

    elif zona == TipoZona.BATALHA:
        if Batalha.objects.filter(partida=partida, rodada=rodada).exists():
            raise ErroBatalhaAtiva("Batalha já criada para está rodada.")
        oponente = Pokemon.objects.filter(ativo=True).order_by("?").first()

        Batalha.objects.create(
            partida=partida,
            rodada=rodada,
            pokemon_jogador=partida.pokemon_inicial,
            pokemon_adversario=oponente,
        )

        payload["oponente_id"] = oponente.id if oponente else None
        payload["oponente_nome"] = oponente.nome if oponente else "???"
        mensagem = f"⚔️ Batalha! Um {oponente.nome} selvagem apareceu!"

    elif zona == TipoZona.NEUTRA:
        mensagem = "😐 Zona Neutra - nada aconteceu"

    EventoRodada.objects.create(
        partida=partida,
        rodada=rodada,
        tipo_evento="zona",
        mensagem_usuario=mensagem,
        payload=payload,
        criado_em=timezone.now(),
    )
    return payload