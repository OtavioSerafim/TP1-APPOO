from flask import render_template

class UserController:
    @staticmethod
    def login():
        return render_template('login.html')
    
    @staticmethod
    def cadastro():
        return render_template('cadastro.html')

