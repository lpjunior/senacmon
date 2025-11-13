from django.utils import timezone
from game.choices import TipoZona
from game.domain.excecoes import ErroBatalhaAtiva
from game.models import Partida, Batalha, Pokemon, EventoRodada
from wallet.services import creditar, debitar


def aplicar_zona(partida: Partida, rodada: int, zona: str, valor_param: int | None) -> dict:
    payload = {"zona": zona, "valor": valor_param}

    if zona == TipoZona.BONUS:
        creditar(partida.user, partida, valor_param or 0, ref_tipo="sistema", ref_id=f"bonus-{rodada}")

    elif zona == TipoZona.PERDA:
        if valor_param:
            debitar(partida.user, partida, abs(valor_param), ref_tipo="sistema", ref_id=f"perda-{rodada}")

    elif zona == TipoZona.CAPTURA:
        partida.rounds_restantes_captura = 2
        partida.save(update_fields=["rounds_restantes_captura", "atualizado_em"])

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

        EventoRodada.objects.create(
            partida=partida,
            rodada=rodada,
            tipo_evento="zona",
            mensagem_usuario="Zona Aplicada",
            payload=payload,
            criado_em=timezone.now(),
        )
    return payload