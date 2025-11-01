import os
from dotenv import load_dotenv
from flask import Flask, g, redirect, url_for, current_app
from models import Models
from controller.user_controller import UserController
from controller.student_controller import StudentController
from controller.auth_controller import AuthController
from utils.errors.erroAutenticacao import ErroAutenticacao

load_dotenv()

app = Flask(
    __name__,
    template_folder=os.path.join('views', 'templates'),
    static_folder=os.path.join('views', 'static'),
    static_url_path='/static'
)

# SECRET_KEY para sessões e flash messages
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
if not app.config['SECRET_KEY']:
    raise ValueError("FLASK_SECRET_KEY não definida. Configure no .env")


DEFAULT_CAPACIDADE_MAXIMA = 100

app.config.setdefault('ACADEMIA_OCUPACAO_ATUAL', 0)
app.config.setdefault('ACADEMIA_CAPACIDADE_MAXIMA', DEFAULT_CAPACIDADE_MAXIMA)
app.config.setdefault('ACADEMIA_PRESENTES', [])


@app.context_processor
def inject_academia_status():
    """Disponibiliza variáveis globais reutilizáveis em todos os templates."""
    presentes = current_app.config.get('ACADEMIA_PRESENTES', [])
    ocupacao_atual = len(presentes)
    current_app.config['ACADEMIA_OCUPACAO_ATUAL'] = ocupacao_atual
    return {
        'alunos_na_academia': ocupacao_atual,
        'capacidade_maxima_academia': current_app.config.get('ACADEMIA_CAPACIDADE_MAXIMA', 0),
        'alunos_presentes': presentes,
    }


@app.before_request
def setup_models():
    g.models = Models()

@app.teardown_request
def teardown_models(exc=None):
    models = getattr(g, "models", None)
    if models is not None:
        models.close()

app.add_url_rule('/cadastro', 'cadastro', UserController.cadastro, methods=['GET', 'POST'])
app.add_url_rule('/', 'login', UserController.login)
app.add_url_rule('/auth/login', 'auth_login', AuthController.login, methods=['POST'])
app.add_url_rule('/gestor', 'gestor', UserController.gestor, methods=['GET', 'POST'])
app.add_url_rule('/gestor/equipamentos', 'equipamentos', UserController.equipamentos)
app.add_url_rule('/gestor/equipamentos/novo', 'cadastro-equipamento', UserController.cadastro_equipamento, methods=['GET', 'POST'])
app.add_url_rule('/gestor/planos', 'planos', UserController.planos)
app.add_url_rule('/gestor/planos/novo', 'cadastro-plano', UserController.cadastro_plano, methods=['GET', 'POST'])
app.add_url_rule('/gestor/alunos', 'alunos-gestor', UserController.alunos_gestor)
app.add_url_rule('/gestor/alunos/novo', 'cadastro-aluno', UserController.cadastro_aluno)
app.add_url_rule('/gestor/entrada', 'autentica-entrada', StudentController.autentica_entrada, methods=['GET'])
app.add_url_rule('/gestor/entrada/registrar', 'registrar_entrada', StudentController.registrar_entrada, methods=['POST'])
app.add_url_rule('/gestor/entrada/saida', 'registrar_saida', StudentController.registrar_saida, methods=['POST'])
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