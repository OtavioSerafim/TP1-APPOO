"""Erros relacionados a validação de dados fornecidos."""

from .erroBase import ErroBase


class ErroDadosInvalidos(ErroBase):
    """Indica que os dados fornecidos não atendem aos requisitos mínimos."""

    def __init__(self, mensagem: str = "Dados inválidos fornecidos."):
        super().__init__(mensagem)
