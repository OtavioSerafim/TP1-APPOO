"""Modelo responsável pelos exercícios cadastrados em fichas."""

from datetime import datetime

from .model import Model


class Exercicio(Model):
    """CRUD especializado para exercícios vinculados a fichas."""

    def __init__(self, connection):
        super().__init__(
            connection,
            table_name="exercicios",
            columns=[
                "id",
                "ficha_id",
                "equipamento_id",
                "nome",
                "series",
                "repeticoes",
                "carga",
                "tempo_descanso",
                "observacoes",
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

    def listar_por_ficha(self, ficha_id):
        query = (
            f"SELECT {', '.join(self.columns)} "
            f"FROM {self.table_name} WHERE ficha_id = ?"
        )
        self.cursor.execute(query, (ficha_id,))
        return self.cursor.fetchall()
