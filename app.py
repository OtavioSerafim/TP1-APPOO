import os
from flask import Flask, g, redirect, url_for
from models import Models
from controller.user_controller import UserController
from controller.auth_controller import AuthController
from utils.errors.erroAutenticacao import ErroAutenticacao

app = Flask(
    __name__,
    template_folder=os.path.join('views', 'templates'),
    static_folder=os.path.join('views', 'static'),
    static_url_path='/static'
)


@app.before_request
def setup_models():
    g.models = Models()

@app.teardown_request
def teardown_models(exc=None):
    models = getattr(g, "models", None)
    if models is not None:
        models.close()

app.add_url_rule('/', 'login', UserController.login)
app.add_url_rule('/cadastro', 'cadastro', UserController.cadastro)
app.add_url_rule('/gestor', 'gestor', UserController.gestor)
app.add_url_rule('/gestor/equipamentos', 'equipamentos', UserController.equipamentos)
app.add_url_rule('/auth/login', 'auth_login', AuthController.login, methods=['POST'])
app.add_url_rule('/auth/logout', 'auth_logout', AuthController.logout, methods=['POST'])


@app.errorhandler(ErroAutenticacao)
def handle_auth_error(_: ErroAutenticacao):
    """Encaminha o usuário para o login quando a sessão não é válida."""
    response = redirect(url_for('login'))
    if getattr(g, 'auth_error_clear_cookie', False):
        response.delete_cookie('auth_token')
        if hasattr(g, 'auth_error_clear_cookie'):
            del g.auth_error_clear_cookie
    return response

if (__name__) == '__main__':
    app.run(debug=True)