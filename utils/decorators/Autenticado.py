"""Decoradores utilitários ligados à autenticação de rotas Flask."""

from __future__ import annotations

import os
from functools import wraps
from typing import Any, Callable, TypeVar

import jwt
from flask import g, request

from utils.errors.erroAutenticacao import ErroAutenticacao
from utils.errors.erroConfiguracao import ErroConfiguracao


F = TypeVar("F", bound=Callable[..., Any])


def autenticado(view_func: F) -> F:
	"""Garante que a rota só execute com um JWT válido."""

	@wraps(view_func)
	def wrapper(*args: Any, **kwargs: Any):
		token = request.cookies.get("auth_token")
		if not token:
			g.auth_error_clear_cookie = True
			raise ErroAutenticacao("Sessão expirada. Faça login novamente.")

		secret = os.getenv("JWT_SECRET")
		if not secret:
			raise ErroConfiguracao("JWT_SECRET não está configurado nas variáveis de ambiente.")

		try:
			payload = jwt.decode(token, secret, algorithms=["HS256"])
		except jwt.ExpiredSignatureError:
			g.auth_error_clear_cookie = True
			raise ErroAutenticacao("Sessão expirada. Faça login novamente.")
		except jwt.InvalidTokenError:
			g.auth_error_clear_cookie = True
			raise ErroAutenticacao("Sessão inválida. Faça login novamente.")

		usuario_model = g.models.usuario
		subject = payload.get("sub")
		try:
			usuario_id = int(subject)
		except (TypeError, ValueError):
			g.auth_error_clear_cookie = True
			raise ErroAutenticacao("Sessão inválida. Faça login novamente.")
		usuario = usuario_model.read(usuario_id)
		if usuario is None:
			g.auth_error_clear_cookie = True
			raise ErroAutenticacao("Usuário não encontrado.")

		g.current_user = usuario
		g.current_user_claims = payload
		return view_func(*args, **kwargs)

	return wrapper


__all__ = ["autenticado"]
