"""Modelo central para fichas de treino."""

from datetime import datetime

from .model import Model


class Ficha(Model):
    """CRUD especializado para fichas associadas a alunos e personais."""

    def __init__(self, connection):
        super().__init__(
            connection,
            table_name="fichas",
            columns=[
                "id",
                "aluno_id",
                "personal_id",
                "descricao",
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

    def listar_por_aluno(self, aluno_id):
        query = f"SELECT {', '.join(self.columns)} FROM {self.table_name} WHERE aluno_id = ?"
        self.cursor.execute(query, (aluno_id,))
        return self.cursor.fetchall()

    def listar_por_personal(self, personal_id):
        query = f"SELECT {', '.join(self.columns)} FROM {self.table_name} WHERE personal_id = ?"
        self.cursor.execute(query, (personal_id,))
        return self.cursor.fetchall()
