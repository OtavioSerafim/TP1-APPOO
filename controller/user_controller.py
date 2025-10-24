from flask import render_template

class UserController:
    @staticmethod
    def login():
        return render_template('login.html')
    
    @staticmethod
    def cadastro():
        return render_template('cadastro.html')
    
    @staticmethod
    def gestor():
        return render_template('home-gestor.html')
    
    @staticmethod
    def equipamentos():
        return render_template('equipamentos.html')

