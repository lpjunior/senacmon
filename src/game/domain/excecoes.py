class ErroDominio(Exception):
    """Erro genérico de domínio."""

class ErroBloqueioCaptura(ErroDominio):
    """Jogador está capturado e não pode jogar."""

class ErroBatalhaAtiva(ErroDominio):
    """Já existe batalha pendente para está rodada."""

class ErroSaldoInsuficiente(ErroDominio):
    """Saldo insuficiente para aposta."""

class ErroApostaInvalida(ErroDominio):
    """Aposta inválida, números ou valores fora das regras."""

class ErroEstadoInvalido(ErroDominio):
    """Operação inválida para o estado atual."""