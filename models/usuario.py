"""Modelo de usuário base, incluindo autenticação e hashing de senha."""

import os
from pathlib import Path
import sys
from datetime import date, datetime, timedelta

import jwt
from bcrypt import checkpw, hashpw, gensalt

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from .model import Model
from utils.errors.erroAutenticacao import ErroAutenticacao
from utils.errors.erroDadosInvalidos import ErroDadosInvalidos
from utils.errors.erroConfiguracao import ErroConfiguracao


class Usuario(Model):
    """Representa usuários com dados comuns a todos os perfis."""

    def __init__(self, connection):
        """Inicializa o modelo apontando para a tabela ``usuarios``."""
        super().__init__(
            connection,
            table_name='usuarios',
            columns=['id', 'nome', 'email', 'senha', 'tipo_usuario', 'criado_em', 'atualizado_em']
        )

    def prepare_create_data(self, data):
        """Aplica hashing à senha e adiciona datas padrão."""
        senha = data.pop('senha', None)
        if senha is None:
            raise ErroDadosInvalidos("Campo 'senha' é obrigatório para criar um usuário.")

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
        """Valida credenciais e retorna um token JWT de sessão."""
        query = (
            f"SELECT id, nome, email, senha, tipo_usuario "
            f"FROM {self.table_name} WHERE email = ?"
        )
        self.cursor.execute(query, (email,))
        user = self.cursor.fetchone()
        if not user:
            raise ErroAutenticacao("Email ou senha inválidos.")

        stored_hash = user[3].encode('utf-8')
        if not checkpw(senha.encode('utf-8'), stored_hash):
            raise ErroAutenticacao("Email ou senha inválidos.")

        secret = os.getenv("JWT_SECRET")
        if not secret:
            raise ErroConfiguracao("JWT_SECRET não está configurado nas variáveis de ambiente.")

        payload = {
            "sub": str(user[0]),
            "nome": user[1],
            "email": user[2],
            "role": user[4],
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=24),
        }
        token = jwt.encode(payload, secret, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token
    
    def read_by_email(self, email):
        """Consulta um usuário pelo email."""
        query = (
            f"SELECT {', '.join(self.columns)} "
            f"FROM {self.table_name} WHERE email = ?"
        )
        self.cursor.execute(query, (email,))
        return self.cursor.fetchone()