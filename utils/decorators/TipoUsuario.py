"""Decoradores que validam o tipo de usuário carregado no contexto."""

from functools import wraps
from typing import Callable, TypeVar

from flask import g

from utils.errors.erroAutenticacao import ErroAutenticacao


F = TypeVar("F", bound=Callable[..., object])


def _obter_tipo_usuario() -> str | None:
	usuario = getattr(g, "current_user", None)
	if usuario is None:
		return None

	if hasattr(usuario, "keys"):
		return usuario.get("tipo_usuario")

	if isinstance(usuario, (tuple, list)) and len(usuario) > 4:
		return usuario[4]

	return None


def gestor_obrigatorio(view_func: F) -> F:
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		tipo = _obter_tipo_usuario()
		if tipo is None:
			raise ErroAutenticacao("Sessão não encontrada. Faça login novamente.")
		if tipo != "gestor":
			raise ErroAutenticacao("Apenas gestores podem acessar esta funcionalidade.")
		return view_func(*args, **kwargs)

	return wrapper  # type: ignore[return-value]


def personal_obrigatorio(view_func: F) -> F:
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		tipo = _obter_tipo_usuario()
		if tipo is None:
			raise ErroAutenticacao("Sessão não encontrada. Faça login novamente.")
		if tipo != "personal":
			raise ErroAutenticacao("Apenas personal trainers podem acessar esta funcionalidade.")
		return view_func(*args, **kwargs)

	return wrapper  # type: ignore[return-value]


__all__ = ["gestor_obrigatorio", "personal_obrigatorio"]
