"""Modelo de usuário base, incluindo autenticação e hashing de senha."""

from datetime import date
from model import Model
from bcrypt import hashpw, gensalt
from ..utils.errors.erroAutenticacao import ErroAutenticacao


class Usuario(Model):
    """Representa usuários com dados comuns a todos os perfis."""

    def __init__(self, connection):
        """Inicializa o modelo apontando para a tabela ``usuarios``."""
        super().__init__(
            connection,
            table_name='usuarios',
            columns=['id', 'nome', 'email', 'tipo_usuario', 'criado_em', 'atualizado_em']
        )

    def prepare_create_data(self, data):
        """Aplica hashing à senha e adiciona datas padrão."""
        senha = data.pop('senha', None)
        if senha is None:
            raise ValueError("Campo 'senha' é obrigatório para criar um usuário.")

        data['senha'] = hashpw(senha.encode('utf-8'), gensalt()).decode('utf-8')
        data.setdefault('criado_em', date.today())
        data.setdefault('atualizado_em', date.today())
        return data

    def prepare_update_data(self, data):
        """Atualiza a senha com hashing e renova ``atualizado_em``."""
        if 'senha' in data:
            data['senha'] = hashpw(data['senha'].encode('utf-8'), gensalt()).decode('utf-8')

        data['atualizado_em'] = date.today()
        return data

    def authenticate(self, email, senha):
        """Valida credenciais retornando dados essenciais do usuário."""
        query = f"SELECT id, nome, email, senha FROM {self.table_name} WHERE email = ?"
        self.cursor.execute(query, (email,))
        user = self.cursor.fetchone()
        if user and hashpw(senha.encode('utf-8'), user[3].encode('utf-8')) == user[3].encode('utf-8'):
            return {'id': user[0], 'nome': user[1], 'email': user[2], 'tipo_usuario': user[3]}
        raise ErroAutenticacao("Email ou senha inválidos.")