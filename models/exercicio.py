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
        """Retorna exercícios de uma ficha com nome do equipamento."""
        query = """
        SELECT 
            e.id, e.ficha_id, e.equipamento_id, e.nome, 
            e.series, e.repeticoes, e.carga, e.tempo_descanso, 
            e.observacoes, e.criado_em, e.atualizado_em,
            eq.nome AS equipamento_nome
        FROM exercicios e
        LEFT JOIN equipamentos eq ON e.equipamento_id = eq.id
        WHERE e.ficha_id = ?
        ORDER BY e.id
        """
        self.cursor.execute(query, (ficha_id,))
        cols = [c[0] for c in self.cursor.description]
        return [dict(zip(cols, row)) for row in self.cursor.fetchall()]