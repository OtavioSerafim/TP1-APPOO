import os
from flask import Flask
from config import Config
from controller.user_controller import UserController

app = Flask(
    __name__,
    template_folder=os.path.join('views', 'templates'),
    static_folder=os.path.join('views', 'static'),
    static_url_path='/static'
)
app.config.from_object(Config)

app.add_url_rule('/', 'login', UserController.login)
app.add_url_rule('/cadastro', 'cadastro', UserController.cadastro)

if (__name__) == '__main__':
    app.run(debug=True)