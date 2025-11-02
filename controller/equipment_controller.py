"""Controlador responsável por atualizações e remoções de equipamentos."""

from __future__ import annotations

from flask import flash, g, redirect, request, url_for

from models.equipamento import Equipamento
from utils.decorators.Autenticado import autenticado
from utils.decorators.TipoUsuario import gestor_obrigatorio
from utils.errors.erroDadosInvalidos import ErroDadosInvalidos


class EquipmentController:
	"""Expõe rotas específicas para editar e remover equipamentos."""

	@staticmethod
	@autenticado
	@gestor_obrigatorio
	def atualizar(equipamento_id: int):
		nome = request.form.get('nome', '').strip()
		valor_raw = request.form.get('valor', '').strip()
		status = request.form.get('status', '').strip()

		if not nome:
			flash('Informe o nome do equipamento.', 'error')
			return redirect(url_for('equipamentos'))

		try:
			valor = float(valor_raw)
			if valor <= 0:
				raise ValueError
		except ValueError:
			flash('Informe um valor válido (maior que zero).', 'error')
			return redirect(url_for('equipamentos'))

		if status not in Equipamento.STATUS_VALIDOS:
			flash('Status inválido. Escolha uma opção permitida.', 'error')
			return redirect(url_for('equipamentos'))

		payload = {
			'nome': nome,
			'valor': valor,
			'status': status,
		}

		try:
			equipamentos_model = g.models.equipamento
			updated = equipamentos_model.update(equipamento_id, payload)
		except ErroDadosInvalidos as err:
			flash(str(err), 'error')
			return redirect(url_for('equipamentos'))
		except Exception as err:
			print(f"Erro ao atualizar equipamento {equipamento_id}: {err}")
			flash('Erro ao atualizar o equipamento. Tente novamente.', 'error')
			return redirect(url_for('equipamentos'))

		if updated == 0:
			flash('Equipamento não encontrado para atualização.', 'error')
		else:
			flash('Equipamento atualizado com sucesso!', 'success')
		return redirect(url_for('equipamentos'))

	@staticmethod
	@autenticado
	@gestor_obrigatorio
	def remover(equipamento_id: int):
		try:
			equipamentos_model = g.models.equipamento
			deleted = equipamentos_model.delete(equipamento_id)
		except Exception as err:
			print(f"Erro ao remover equipamento {equipamento_id}: {err}")
			flash('Erro ao remover o equipamento. Tente novamente.', 'error')
			return redirect(url_for('equipamentos'))

		if deleted == 0:
			flash('Equipamento não encontrado para remoção.', 'error')
		else:
			flash('Equipamento removido com sucesso!', 'success')
		return redirect(url_for('equipamentos'))


__all__ = ['EquipmentController']
