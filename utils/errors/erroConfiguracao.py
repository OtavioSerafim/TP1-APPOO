"""Erros relacionados a configurações ausentes ou inválidas."""

from .erroBase import ErroBase


class ErroConfiguracao(ErroBase):
    """Erro lançado quando a aplicação está configurada de maneira incorreta."""

    def __init__(self, mensagem: str = "Configuração inválida ou ausente."):
        super().__init__(mensagem)
