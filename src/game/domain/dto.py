from dataclasses import dataclass
from typing import Any

@dataclass
class ResultadoRolagem:
    dado: int
    posicao_antiga: int
    posicao_nova: int
    zona: str
    dados_zona: dict[str, Any]

@dataclass
class PreviaBatalha:
    nome_oponente: str
    elemento_oponente: str
    minimo_simples: int
    minimo_dupla: int
    base_simples: float
    base_dupla: float
    elemento_jogador: str

@dataclass
class ResolucaoBatalha:
    numero_sorteado: int
    resultado: str
    multiplicador_efetivo: float
    delta_berries: int
    resumo: dict