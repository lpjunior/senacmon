import random
from typing import Tuple

def seed_rodada(id_partida: int, rodada: int) -> str:
    return f"P{id_partida}-R{rodada}"

def sorteio_dado(seed: str) -> Tuple[int, int]:
    r = random.Random(seed + '-die')
    return 1, r.randint(1, 6)

def sorteio_numero(seed: str, low: int = 0, high: int = 9) -> int:
    r = random.Random(seed + '-draw')
    return r.randint(low, high)