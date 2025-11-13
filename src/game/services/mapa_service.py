from typing import Tuple
from game.models import Partida, MapaPosicao

def obter_zona_da_posicao(partida: Partida, posicao: int) -> Tuple[str, int | None]:
    mp = MapaPosicao.objects.get(mapa=partida.mapa, posicao=posicao)
    return mp.tipo_zona, mp.valor_param

def avancar_posicao(atual: int, passos: int, tamanho: int) -> int:
    nova = atual + passos
    if nova > tamanho:
        nova = ((nova - 1) % tamanho) + 1
    return nova