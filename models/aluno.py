"""Modelos responsáveis por estender ``Usuario`` com dados específicos de alunos."""

from datetime import datetime

from .model import Model
from .usuario import Usuario


class _AlunoModel(Model):
    """CRUD auxiliar para tabela `alunos` com valores padrão."""

    def __init__(self, connection):
        """Configura o modelo auxiliar para acessar a tabela ``alunos``."""
        super().__init__(
            connection,
            table_name='alunos',
            columns=[
                'id',
                'face_embedding',
                'data_ultima_entrada',
                'personal_id',
                'plano_id',
                'plano_data_inicio',
            ],
            primary_key='id'
        )

    def prepare_create_data(self, data):
        """Garante um timestamp padrão para novos registros."""
        payload = super().prepare_create_data(data)
        payload.setdefault('data_ultima_entrada', datetime.now().isoformat())
        return payload

    def prepare_update_data(self, data):
        """Atualiza o timestamp quando houver mudança em dados específicos."""
        payload = super().prepare_update_data(data)
        if not payload:
            return payload
        payload.setdefault('data_ultima_entrada', datetime.now().isoformat())
        return payload


class Aluno(Usuario):
    """Modelo de domínio para alunos, agregando dados extras ao usuário base."""

    def __init__(self, connection):
        """Cria o modelo composto com acesso às tabelas ``usuarios`` e ``alunos``."""
        super().__init__(connection)
        self._aluno_model = _AlunoModel(connection)

    def create(self, data):
        """Cria o usuário e persiste as informações específicas de aluno."""
        aluno_data = {
            'face_embedding': data.pop('face_embedding', None),
            'data_ultima_entrada': data.pop('data_ultima_entrada', None),
            'personal_id': data.pop('personal_id', None),
            'plano_id': data.pop('plano_id', None),
            'plano_data_inicio': data.pop('plano_data_inicio', None),
        }
        data['tipo_usuario'] = 'aluno'
        usuario_id = super().create(data)

        aluno_payload = {k: v for k, v in aluno_data.items() if v is not None}
        aluno_payload['id'] = usuario_id
        self._aluno_model.create(aluno_payload)
        return usuario_id

    def get_all(self):
        """Retorna todos os alunos com seus dados completos (usuário + aluno)."""
        query = """
        SELECT 
            u.id, u.nome, u.email,
            a.personal_id, a.plano_id, a.plano_data_inicio,
            strftime('%Y-%m-%d às %H:%M', a.data_ultima_entrada) AS data_ultima_entrada,
            p.nome AS plano_nome
        FROM usuarios u
        INNER JOIN alunos a ON u.id = a.id
        LEFT JOIN planos p ON a.plano_id = p.id
        WHERE u.tipo_usuario = 'aluno'
        ORDER BY u.nome
        """
        self.cursor.execute(query)
        cols = [col[0] for col in self.cursor.description]
        return [dict(zip(cols, row)) for row in self.cursor.fetchall()]

    def read(self, usuario_id):
        """Consulta dados do usuário e complementos do aluno."""
        usuario = super().read(usuario_id)
        if not usuario:
            return None

        aluno_extra = self._aluno_model.read(usuario_id)
        return {
            'usuario': usuario,
            'aluno': aluno_extra
        }

    def update(self, usuario_id, data):
        """Sincroniza alterações entre a base de usuários e o detalhe de alunos."""
        aluno_data = {
            k: data.pop(k)
            for k in ['face_embedding', 'data_ultima_entrada', 'personal_id', 'plano_id', 'plano_data_inicio']
            if k in data
        }
        updated_rows = 0

        if any(key in data for key in ['nome', 'email']):
            usuario_atual = super().read(usuario_id)
            if not usuario_atual:
                return 0

            nome = data.get('nome', usuario_atual[1])
            email = data.get('email', usuario_atual[2])
            updated_rows = super().update(usuario_id, {'nome': nome, 'email': email})

        if aluno_data:
            aluno_result = self._aluno_model.update(usuario_id, aluno_data)
            updated_rows = max(updated_rows, aluno_result)

        return updated_rows

    def delete(self, usuario_id):
        """Remove o aluno garantindo exclusão dos dados extras vinculados."""
        self._aluno_model.delete(usuario_id)
        return super().delete(usuario_id)
