import os
from flask import Flask, g
from models import Models
from controller.user_controller import UserController

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

if (__name__) == '__main__':
    app.run(debug=True)