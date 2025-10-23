"""Facilita importações diretas dos modelos e do contexto compartilhado."""

from .model import Model
from .usuario import Usuario
from .aluno import Aluno
from .personal import Personal
from .gestor import Gestor
from .equipamento import Equipamento
from .ficha import Ficha
from .exercicio import Exercicio
from .plano import Plano
from .main import Models

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
    "Models",
]
