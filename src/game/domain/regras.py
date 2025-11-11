from dataclasses import dataclass

@dataclass(frozen=True)
class PoliticaMultiplicador:
    base_simples: float = 3.0
    base_dupla: float = 1.8
    bonus_vantagem: float = 0.2
    penalidade_desvantagem: float = 0.2
    minimo_efetivo: float = 0.2

def resultado_elemental(elem_jogador: str, elem_oponente: str) -> str:
    if elem_jogador == "fogo" and elem_oponente == "planta":
        return "vantagem"
    if elem_jogador == "agua" and elem_oponente == "fogo":
        return "vantagem"
    if elem_jogador == "planta" and elem_oponente == "agua":
        return "vantagem"
    if elem_jogador == elem_oponente:
        return "neutro"
    return "desvantagem"

def multiplicador_efetivo(qtd_escolhas: int, resultado: str, politica: PoliticaMultiplicador) -> float:
    base = politica.base_simples if qtd_escolhas == 1 else politica.base_dupla

    if resultado == "vantagem":
        efetivo = base + politica.bonus_vantagem
    elif resultado == "desvantagem":
        efetivo = base - politica.penalidade_desvantagem
    else:
        efetivo = base

    return max(efetivo, politica.minimo_efetivo)