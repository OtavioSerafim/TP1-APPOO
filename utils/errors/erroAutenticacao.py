from erroBase import ErroBase

class ErroAutenticacao(ErroBase):
    """Erro de autenticação."""

    def __init__(self, mensagem: str):
        super().__init__(mensagem)