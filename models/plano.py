"""Modelo responsável por gerenciar planos de assinatura de alunos."""

from datetime import datetime

from .model import Model


class Plano(Model):
    """CRUD especializado para planos disponíveis na academia."""

    def __init__(self, connection):
        super().__init__(
            connection,
            table_name="planos",
            columns=[
                "id",
                "nome",
                "descricao",
                "valor_mensal",
                "duracao_meses",
                "criado_em",
                "atualizado_em",
            ],
        )

    def prepare_create_data(self, data):
        payload = super().prepare_create_data(data)
        agora = datetime.now().isoformat()
        payload.setdefault("criado_em", agora)
        payload.setdefault("atualizado_em", agora)
        return payload

    def prepare_update_data(self, data):
        payload = super().prepare_update_data(data)
        if payload:
            payload["atualizado_em"] = datetime.now().isoformat()
        return payload

    def possui_alunos_associados(self, plano_id: int) -> bool:
        """Retorna True se existir ao menos um aluno vinculado ao plano informado."""
        query = "SELECT 1 FROM alunos WHERE plano_id = ? LIMIT 1"
        self.cursor.execute(query, (plano_id,))
        return self.cursor.fetchone() is not None
