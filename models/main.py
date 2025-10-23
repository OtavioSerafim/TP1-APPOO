"""Contexto leve para instanciar modelos com uma única conexão."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict

from .model import Model
from .usuario import Usuario
from .aluno import Aluno
from .personal import Personal
from .gestor import Gestor
from .equipamento import Equipamento
from .ficha import Ficha
from .exercicio import Exercicio
from .plano import Plano


DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "database" / "app.db"


class Models:
    """Mantém uma única conexão SQLite e modelos compartilhados."""

    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH) -> None:
        self.db_path = Path(db_path)
        self._connection = sqlite3.connect(self.db_path)
        self._connection.row_factory = sqlite3.Row
        self._models: Dict[str, Model] = {
            "usuario": Usuario(self._connection),
            "aluno": Aluno(self._connection),
            "personal": Personal(self._connection),
            "gestor": Gestor(self._connection),
            "equipamento": Equipamento(self._connection),
            "ficha": Ficha(self._connection),
            "exercicio": Exercicio(self._connection),
            "plano": Plano(self._connection),
        }

    
    """Acessos"""   
    
    @property
    def connection(self) -> sqlite3.Connection:
        return self._connection

    def get(self, name: str) -> Model:
        return self._models[name.lower()]

    @property
    def usuario(self) -> Usuario:
        return self._models["usuario"]

    @property
    def aluno(self) -> Aluno:
        return self._models["aluno"]

    @property
    def personal(self) -> Personal:
        return self._models["personal"]

    @property
    def gestor(self) -> Gestor:
        return self._models["gestor"]

    @property
    def equipamento(self) -> Equipamento:
        return self._models["equipamento"]

    @property
    def ficha(self) -> Ficha:
        return self._models["ficha"]

    @property
    def exercicio(self) -> Exercicio:
        return self._models["exercicio"]

    @property
    def plano(self) -> Plano:
        return self._models["plano"]

    def close(self) -> None:
        self._connection.close()


__all__ = [
    "Models",
]
