"""Exposição direta dos modelos de domínio para importações simples."""

from .model import Model
from .usuario import Usuario
from .aluno import Aluno
from .personal import Personal
from .gestor import Gestor
from .equipamento import Equipamento
from .ficha import Ficha
from .exercicio import Exercicio
from .plano import Plano

__all__ = [
    "Model",
    "Usuario",
    "Aluno",
    "Personal",
    "Gestor",
    "Equipamento",
    "Ficha",
    "Exercicio",
    "Plano",
]
