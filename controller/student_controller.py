from flask import (
	current_app,
	flash,
	g,
	redirect,
	render_template,
	request,
	url_for,
)

from utils.decorators.Autenticado import autenticado
from utils.errors.erroDadosInvalidos import ErroDadosInvalidos


class StudentController:
	@staticmethod
	@autenticado
	def autentica_entrada():
		termo_busca = request.args.get('q', '').strip()
		resultados = []
		if termo_busca:
			linhas = g.models.aluno.buscar_por_nome_ou_email(termo_busca)
			resultados = [StudentController._row_to_dict(linha) for linha in linhas]

		presentes = StudentController._get_alunos_presentes()
		return render_template(
			'autentica-entrada.html',
			usuario=g.current_user,
			termo_busca=termo_busca,
			resultados=resultados,
			presentes=presentes,
			capacidade_maxima=current_app.config.get('ACADEMIA_CAPACIDADE_MAXIMA', 0),
		)

	@staticmethod
	@autenticado
	def registrar_entrada():
		redirect_response = StudentController._redirect_back_to_list()

		aluno_id_raw = request.form.get('aluno_id', '').strip()
		if not aluno_id_raw:
			flash('Selecione um aluno para registrar a entrada.', 'error')
			return redirect_response

		try:
			aluno_id = int(aluno_id_raw)
		except ValueError:
			flash('Identificador de aluno inválido.', 'error')
			return redirect_response

		aluno_detalhe = g.models.aluno.read(aluno_id)
		if not aluno_detalhe or aluno_detalhe.get('usuario') is None:
			flash('Aluno não encontrado.', 'error')
			return redirect_response

		presentes = StudentController._get_alunos_presentes(raw=True)
		if any(presente['id'] == aluno_id for presente in presentes):
			flash('Este aluno já está marcado como presente.', 'error')
			return redirect_response

		capacidade_maxima = current_app.config.get('ACADEMIA_CAPACIDADE_MAXIMA', 0)
		if capacidade_maxima and len(presentes) >= capacidade_maxima:
			flash('Capacidade máxima atingida. Não é possível registrar nova entrada.', 'error')
			return redirect_response

		try:
			instante = g.models.aluno.registrar_entrada(aluno_id)
		except ErroDadosInvalidos as error:
			flash(str(error), 'error')
			return redirect_response

		usuario_row = StudentController._row_to_dict(aluno_detalhe['usuario'])
		presentes.append({
			'id': aluno_id,
			'nome': usuario_row['nome'],
			'email': usuario_row['email'],
			'entrada_em': instante,
		})
		StudentController._persist_presencas(presentes)

		flash('Entrada registrada com sucesso!', 'success')
		return redirect_response

	@staticmethod
	@autenticado
	def registrar_saida():
		redirect_response = StudentController._redirect_back_to_list()

		aluno_id_raw = request.form.get('aluno_id', '').strip()
		if not aluno_id_raw:
			flash('Selecione um aluno para registrar a saída.', 'error')
			return redirect_response

		try:
			aluno_id = int(aluno_id_raw)
		except ValueError:
			flash('Identificador de aluno inválido.', 'error')
			return redirect_response

		presentes = StudentController._get_alunos_presentes(raw=True)
		novos_presentes = [p for p in presentes if p['id'] != aluno_id]
		if len(novos_presentes) == len(presentes):
			flash('Este aluno não está marcado como presente.', 'error')
			return redirect_response

		StudentController._persist_presencas(novos_presentes)
		flash('Saída registrada com sucesso!', 'success')
		return redirect_response

	@staticmethod
	def _row_to_dict(row):
		if row is None:
			return {}
		if hasattr(row, 'keys'):
			return {chave: row[chave] for chave in row.keys()}
		return dict(row)

	@staticmethod
	def _get_alunos_presentes(raw=False):
		presentes = current_app.config.setdefault('ACADEMIA_PRESENTES', [])
		return presentes if raw else list(presentes)

	@staticmethod
	def _persist_presencas(presentes):
		current_app.config['ACADEMIA_PRESENTES'] = presentes
		current_app.config['ACADEMIA_OCUPACAO_ATUAL'] = len(presentes)

	@staticmethod
	def _redirect_back_to_list():
		termo = request.form.get('context_query', '').strip()
		if termo:
			return redirect(url_for('autentica-entrada', q=termo))
		return redirect(url_for('autentica-entrada'))
