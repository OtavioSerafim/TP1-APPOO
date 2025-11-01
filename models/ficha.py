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
    
    def get_all(self):
        """Sobrescreve get_all() incluindo nomes de aluno e personal."""
        query = """
        SELECT 
            f.id, f.aluno_id, f.personal_id, f.descricao, 
            f.criado_em, f.atualizado_em,
            a.nome AS aluno_nome,
            p.nome AS personal_nome
        FROM fichas f
        INNER JOIN usuarios a ON f.aluno_id = a.id
        INNER JOIN usuarios p ON f.personal_id = p.id
        ORDER BY f.id DESC
        """
        self.cursor.execute(query)
        cols = [c[0] for c in self.cursor.description]
        return [dict(zip(cols, row)) for row in self.cursor.fetchall()]

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

    def listar_por_id(self, ficha_id):
        query = """
        SELECT 
            f.id, f.aluno_id, f.personal_id, f.descricao, 
            f.criado_em, f.atualizado_em,
            a.nome AS aluno_nome,
            p.nome AS personal_nome
        FROM fichas f
        INNER JOIN usuarios a ON f.aluno_id = a.id
        INNER JOIN usuarios p ON f.personal_id = p.id
        WHERE f.id = ?
        """
        self.cursor.execute(query, (ficha_id,))
        row = self.cursor.fetchone()
        if not row:
            return None
        cols = [c[0] for c in self.cursor.description]
        return dict(zip(cols, row))