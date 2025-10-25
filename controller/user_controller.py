from flask import render_template

from utils.decorators.Autenticado import autenticado

class UserController:
    @staticmethod
    def login():
        return render_template('login.html')
    
    @staticmethod
    def cadastro():
        return render_template('cadastro.html')
    
    @staticmethod
    @autenticado
    def gestor():
        return render_template('home-gestor.html')
    
    @staticmethod
    @autenticado
    def equipamentos():
        return render_template('equipamentos.html')

