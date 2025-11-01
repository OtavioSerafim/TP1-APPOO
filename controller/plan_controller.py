"""Controlador especializado em operações sobre planos."""

from __future__ import annotations

from flask import flash, g, redirect, request, url_for

from utils.decorators.Autenticado import autenticado
from utils.errors.erroDadosInvalidos import ErroDadosInvalidos


class PlanController:
	"""Expõe ações de atualização e remoção de planos para gestores."""

	@staticmethod
	@autenticado
	def atualizar(plano_id: int):
		"""Processa a atualização de um plano existente."""
		nome = request.form.get('nome', '').strip()
		descricao = request.form.get('descricao', '').strip()
		valor_raw = request.form.get('valor_mensal', '').strip()
		duracao_raw = request.form.get('duracao_meses', '').strip()

		if not nome:
			flash('Informe o nome do plano.', 'error')
			return redirect(url_for('planos'))

		try:
			valor = float(valor_raw)
			if valor <= 0:
				raise ValueError
		except ValueError:
			flash('Informe um valor mensal válido (maior que zero).', 'error')
			return redirect(url_for('planos'))

		try:
			duracao = int(duracao_raw)
			if duracao <= 0:
				raise ValueError
		except ValueError:
			flash('Informe uma duração em meses válida (inteiro positivo).', 'error')
			return redirect(url_for('planos'))

		payload = {
			'nome': nome,
			'descricao': descricao,
			'valor_mensal': f"{valor:.2f}",
			'duracao_meses': duracao,
		}

		try:
			planos_model = g.models.plano
			updated = planos_model.update(plano_id, payload)
		except ErroDadosInvalidos as err:
			flash(str(err), 'error')
			return redirect(url_for('planos'))
		except Exception as err:
			print(f"Erro ao atualizar plano {plano_id}: {err}")
			flash('Erro ao atualizar o plano. Tente novamente.', 'error')
			return redirect(url_for('planos'))

		if updated == 0:
			flash('Plano não encontrado para atualização.', 'error')
		else:
			flash('Plano atualizado com sucesso!', 'success')
		return redirect(url_for('planos'))

	@staticmethod
	@autenticado
	def remover(plano_id: int):
		"""Remove um plano do catálogo."""
		try:
			planos_model = g.models.plano
			if planos_model.possui_alunos_associados(plano_id):
				flash('Não é possível remover este plano porque há alunos vinculados a ele.', 'error')
				return redirect(url_for('planos'))
		except Exception as err:
			print(f"Erro ao verificar vínculos do plano {plano_id}: {err}")
			flash('Erro ao validar vínculos do plano. Tente novamente.', 'error')
			return redirect(url_for('planos'))
		try:
			deleted = planos_model.delete(plano_id)
		except Exception as err:
			print(f"Erro ao remover plano {plano_id}: {err}")
			flash('Erro ao remover o plano. Tente novamente.', 'error')
			return redirect(url_for('planos'))

		if deleted == 0:
			flash('Plano não encontrado para remoção.', 'error')
		else:
			flash('Plano removido com sucesso!', 'success')
		return redirect(url_for('planos'))


__all__ = ['PlanController']
