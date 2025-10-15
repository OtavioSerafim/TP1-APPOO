class ErroBase(Exception):
    """Classe base para erros personalizados."""

    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem

    def __str__(self):
        return self.mensagem