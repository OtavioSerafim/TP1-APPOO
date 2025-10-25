"""Controlador responsável pela autenticação de usuários."""

from flask import g, jsonify, make_response, request

from utils.errors.erroAutenticacao import ErroAutenticacao
from utils.errors.erroConfiguracao import ErroConfiguracao
from utils.errors.erroDadosInvalidos import ErroDadosInvalidos


class AuthController:
	"""Expõe rotas ligadas à autenticação."""

	@staticmethod
	def login():
		"""Processa credenciais e devolve um cookie com o JWT."""
		body = request.get_json(silent=True) or request.form.to_dict()
		email = (body.get("email") or "").strip()
		senha = body.get("senha")

		if not email or not senha:
			return jsonify({"message": "Campos 'email' e 'senha' são obrigatórios."}), 400

		try:
			usuario_model = g.models.usuario
			token = usuario_model.authenticate(email, senha)
		except ErroAutenticacao as err:
			return jsonify({"message": str(err)}), 401
		except ErroDadosInvalidos as err:
			return jsonify({"message": str(err)}), 400
		except ErroConfiguracao as err:
			return jsonify({"message": str(err)}), 500
		except Exception:
			# Resposta genérica para evitar vazar detalhes sensíveis.
			return jsonify({"message": "Falha ao autenticar o usuário."}), 500

		response = make_response(jsonify({"message": "Autenticado com sucesso."}))
		response.set_cookie(
			"auth_token",
			token,
			max_age=24 * 60 * 60,
			httponly=True,
			secure=False,
			samesite="Lax",
		)
		return response

	@staticmethod
	def logout():
		"""Revoga a sessão removendo o cookie JWT."""
		response = make_response(jsonify({"message": "Sessão encerrada."}))
		response.delete_cookie("auth_token")
		return response


__all__ = ["AuthController"]
