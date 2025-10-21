"""Modelos responsáveis por estender ``Usuario`` com dados específicos de gestores."""

from datetime import datetime

from .model import Model
from .usuario import Usuario


class _GestorModel(Model):
	"""CRUD auxiliar para tabela `gestores` com valores padrão."""

	def __init__(self, connection):
		"""Configura o modelo auxiliar para acessar a tabela ``gestores``."""
		super().__init__(
			connection,
			table_name='gestores',
			columns=['id', 'data_ultima_atualizacao'],
			primary_key='id'
		)

	def prepare_create_data(self, data):
		"""Garante um timestamp padrão para novos registros."""
		payload = super().prepare_create_data(data)
		payload.setdefault('data_ultima_atualizacao', datetime.now().isoformat())
		return payload

	def prepare_update_data(self, data):
		"""Atualiza o timestamp quando houver mudança em dados específicos."""
		payload = super().prepare_update_data(data)
		if not payload:
			return payload
		payload.setdefault('data_ultima_atualizacao', datetime.now().isoformat())
		return payload


class Gestor(Usuario):
	"""Modelo de domínio para gestores, agregando dados extras ao usuário base."""

	def __init__(self, connection):
		"""Cria o modelo composto com acesso às tabelas ``usuarios`` e ``gestores``."""
		super().__init__(connection)
		self._gestor_model = _GestorModel(connection)

	def create(self, data):
		"""Cria o usuário e persiste as informações específicas do gestor."""
		gestor_data = {
			'data_ultima_atualizacao': data.pop('data_ultima_atualizacao', None)
		}
		data['tipo_usuario'] = 'gestor'
		usuario_id = super().create(data)

		gestor_payload = {k: v for k, v in gestor_data.items() if v is not None}
		gestor_payload['id'] = usuario_id
		self._gestor_model.create(gestor_payload)
		return usuario_id

	def read(self, usuario_id):
		"""Consulta dados do usuário e complementos do gestor."""
		usuario = super().read(usuario_id)
		if not usuario:
			return None

		gestor_extra = self._gestor_model.read(usuario_id)
		return {
			'usuario': usuario,
			'gestor': gestor_extra
		}

	def update(self, usuario_id, data):
		"""Sincroniza alterações entre a base de usuários e o detalhe de gestor."""
		gestor_data = {k: data.pop(k) for k in ['data_ultima_atualizacao'] if k in data}
		updated_rows = 0

		if any(key in data for key in ['nome', 'email']):
			usuario_atual = super().read(usuario_id)
			if not usuario_atual:
				return 0

			nome = data.get('nome', usuario_atual[1])
			email = data.get('email', usuario_atual[2])
			updated_rows = super().update(usuario_id, {'nome': nome, 'email': email})

		if gestor_data:
			gestor_result = self._gestor_model.update(usuario_id, gestor_data)
			updated_rows = max(updated_rows, gestor_result)

		return updated_rows

	def delete(self, usuario_id):
		"""Remove o gestor garantindo exclusão dos dados extras vinculados."""
		self._gestor_model.delete(usuario_id)
		return super().delete(usuario_id)

