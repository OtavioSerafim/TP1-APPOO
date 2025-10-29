from flask import render_template

from utils.decorators.Autenticado import autenticado

class UserController:
    @staticmethod
    # tela de login de um usuário no programa
    def login():
        return render_template('login.html')
    
    # tela de cadastro de um usuário do programa
    @staticmethod
    def cadastro():
        return render_template('cadastro.html')
    
    # tela incial - versaõ do gestor
    @staticmethod
    @autenticado
    def gestor():
        return render_template('home-gestor.html')
    
    # tela de gestão e visualização de equipamentos - exclusiva do gestor
    @staticmethod
    @autenticado
    def equipamentos():
        return render_template('equipamentos.html')

    # tela de cadastro de equipamentos - exclusiva do gestor
    @staticmethod
    def cadastro_equipamento():
        return render_template('cadastro-equipamento.html')
    
    # tela de gerenciamento dos alunos - versão do gestor
    @staticmethod
    def alunos_gestor():
        return render_template('alunos-gestor.html')
    
    #tela de cadastro de alunos - exclusiva do gestor
    @staticmethod
    def cadastro_aluno():
        return render_template('cadastro-aluno.html')
    
    #tela de gerenciamento dos planos - exclusiva do gestor
    @staticmethod
    def planos():
        return render_template('planos.html')
    
    #tela de autenticação da entrada dos alunos - exclusiva do gestor
    @staticmethod
    def autentica_entrada():
        return render_template('autentica-entrada.html')