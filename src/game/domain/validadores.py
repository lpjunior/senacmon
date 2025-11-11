from game.domain.excecoes import ErroBloqueioCaptura, ErroBatalhaAtiva, ErroApostaInvalida

def garantir_nao_capturado(rodadas_restantes_captura: int):
    if rodadas_restantes_captura > 0:
        raise ErroBloqueioCaptura("Você está capturado por N rodadas.")

def garantir_sem_batalha_ativa(pendente: bool):
    if pendente:
        raise ErroBatalhaAtiva("Há batalha pendente para esta rodada.")

def validar_aposta(numeros: list[int], valor: int, minimo_simples: int, minimo_dupla: int, teto_rodada:int):
    if not numeros or len(numeros) not in (1, 2):
        raise ErroApostaInvalida("Escolha 1 ou 2 números.")
    if len(numeros) == 1 and valor < minimo_simples:
        raise ErroApostaInvalida("Aposta abaixo do mínimo para 1 número.")
    if len(numeros) == 2 and valor < minimo_dupla:
        raise ErroApostaInvalida("Aposta abaixo do mínimo para 2 números.")
    if valor > teto_rodada:
        raise ErroApostaInvalida("Aposta acima do teto da rodada.")