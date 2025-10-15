"""Interfaces e comportamentos base para modelos de persistência."""

from abc import ABC, abstractmethod

class modelBase(ABC):
    """Define operações CRUD obrigatórias para modelos concretos."""

    def __init__(self, connection):
        """Armazena a conexão e cria um cursor reutilizável."""
        self.connection = connection
        self.cursor = connection.cursor()

    @abstractmethod
    def create(self, data):
        """Insere um novo registro usando os valores de ``data``."""
        pass

    @abstractmethod
    def read(self, id):
        """Retorna um registro correspondente ao identificador informado."""
        pass

    @abstractmethod
    def update(self, id, data):
        """Atualiza o registro ``id`` com os valores providos em ``data``."""
        pass

    @abstractmethod
    def delete(self, id):
        """Remove o registro identificado por ``id``."""
        pass