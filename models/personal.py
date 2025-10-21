"""Modelos responsáveis por estender ``Usuario`` com dados específicos de personal."""

from datetime import datetime

from .model import Model
from .usuario import Usuario


class _PersonalModel(Model):
	"""CRUD auxiliar para tabela `personais` com valores padrão."""

	def __init__(self, connection):
		"""Configura o modelo auxiliar para acessar a tabela ``personais``."""
		super().__init__(
			connection,
			table_name='personais',
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


class Personal(Usuario):
	"""Modelo de domínio para personal trainers, agregando dados extras ao usuário base."""

	def __init__(self, connection):
		"""Cria o modelo composto com acesso às tabelas ``usuarios`` e ``personais``."""
		super().__init__(connection)
		self._personal_model = _PersonalModel(connection)

	def create(self, data):
		"""Cria o usuário e persiste as informações específicas do personal."""
		personal_data = {
			'data_ultima_atualizacao': data.pop('data_ultima_atualizacao', None)
		}
		data['tipo_usuario'] = 'personal'
		usuario_id = super().create(data)

		personal_payload = {k: v for k, v in personal_data.items() if v is not None}
		personal_payload['id'] = usuario_id
		self._personal_model.create(personal_payload)
		return usuario_id

	def read(self, usuario_id):
		"""Consulta dados do usuário e complementos do personal."""
		usuario = super().read(usuario_id)
		if not usuario:
			return None

		personal_extra = self._personal_model.read(usuario_id)
		return {
			'usuario': usuario,
			'personal': personal_extra
		}

	def update(self, usuario_id, data):
		"""Sincroniza alterações entre a base de usuários e o detalhe de personal."""
		personal_data = {k: data.pop(k) for k in ['data_ultima_atualizacao'] if k in data}
		updated_rows = 0

		if any(key in data for key in ['nome', 'email']):
			usuario_atual = super().read(usuario_id)
			if not usuario_atual:
				return 0

			nome = data.get('nome', usuario_atual[1])
			email = data.get('email', usuario_atual[2])
			updated_rows = super().update(usuario_id, {'nome': nome, 'email': email})

		if personal_data:
			personal_result = self._personal_model.update(usuario_id, personal_data)
			updated_rows = max(updated_rows, personal_result)

		return updated_rows

	def delete(self, usuario_id):
		"""Remove o personal garantindo exclusão dos dados extras vinculados."""
		self._personal_model.delete(usuario_id)
		return super().delete(usuario_id)

