from flask import render_template

class UserController:
    @staticmethod
    def login():
        return render_template('login.html')

