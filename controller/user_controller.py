from flask import render_template

class UserController:
    @staticmethod
    def index():
        return render_template('index.html')

