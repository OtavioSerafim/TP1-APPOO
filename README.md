# TP1-APPOO — Backend Orientado a Objetos para Gestão de Academia

Projeto backend desenvolvido como trabalho prático da disciplina **Análise, Projeto e Programação Orientados a Objetos (APPOO)**. A aplicação implementa o núcleo de negócios de uma academia, com foco em modelagem orientada a objetos, regras de autenticação, gerenciamento de usuários, planos e equipamentos. O Flask é utilizado como camada de entrega HTTP, expondo o domínio por meio de templates e rotas finas.

## 🧭 Contexto acadêmico
O objetivo central é comprovar, na prática, os conceitos de orientação a objetos vistos na disciplina: herança, composição, classes abstratas, reutilização de lógica e encapsulamento. A stack (Python + SQLite) foi escolhida por ser acessível e por atender aos requisitos definidos pela disciplina, que estabelece o uso de Python como linguagem base para o desenvolvimento. O Flask atua como ponte leve entre as camadas. Todo o comportamento de domínio permanece isolado em classes Python.

## 🎯 Foco em backend orientado a objetos
- **Modelos especializados** (`Aluno`, `Personal`, `Gestor`, `Equipamento`, `Plano`, `Ficha`, `Exercicio`) estendem uma classe base (`Model`) que fornece CRUD genérico, reduzindo duplicação.
- **Classe `Models` como contexto compartilhado**, centralizando a conexão SQLite e entregando instâncias prontas de cada modelo por requisição.
- **Decoradores e erros customizados** (`@autenticado`, `ErroAutenticacao`, `ErroDadosInvalidos`, `ErroConfiguracao`) implementam regras transversais sem acoplar lógica às rotas.
- **Separação de preocupações** Controllers apenas orquestram requisições e delegam as regras de negócio para os modelos, mantendo o Flask como camada de interface mínima.

## 🚀 Visão geral da aplicação
- Núcleo orientado a objetos para **cadastro e autenticação** de gestores e personal trainers.
- Regras de sessão baseadas em **JWT** com hashing de senha (`bcrypt`) encapsulado em `models.Usuario`.
- Serviços de domínio para **listar, cadastrar e atualizar** equipamentos, planos, fichas e exercícios.
- Estrutura pronta para extensão de turmas, relatórios e dashboards específicos de personal, mantendo a lógica no backend.
- Monitoramento da ocupação da academia via contexto global, alimentando templates com dados em tempo real.

## 🧱 Arquitetura em camadas
A aplicação adota uma separação clara de responsabilidades:

- `app.py`: configura o Flask, registra rotas, fornece um contexto de modelos por requisição via `g.models` e expõe dados globais de ocupação da academia através de um *context processor*.
- `controller/`: camadas de controle (`UserController`, `AuthController`, `StudentController`, `PlanController`, `EquipmentController`) que recebem requisições HTTP, realizam validações mínimas e delegam decisões aos modelos.
- `models/`: camada de persistência em SQLite com classes que herdam de uma base `Model`. Há modelos compostos (`Aluno`, `Personal`, `Gestor`) que estendem `Usuario` para compartilhar comportamento.
- `views/`: templates Jinja2 e assets estáticos usados apenas para renderizar o resultado das regras de negócio encapsuladas no backend.
- `utils/`: decoradores e classes de erro que padronizam autenticação, mensagens e validação de dados.

### 📚 Documentação complementar
- [Visão rápida dos models](docs/models.md)
- [Resumo do banco de dados](docs/database.md)
- [Catálogo de erros personalizados](docs/erros.md)
- [Configuração do app Flask](docs/app.md)
- [Camada de controllers](docs/controllers.md)
- [Overview das views](docs/views.md)
- [Decorators de autenticação](docs/decorators.md)

### Contexto de modelos compartilhado
O arquivo `models/main.py` define a classe `Models`, responsável por abrir uma única conexão SQLite por requisição e expor instâncias de cada modelo (usuários, alunos, planos, equipamentos etc.). Essa conexão é criada em `@app.before_request` e encerrada em `@app.teardown_request`, garantindo encapsulamento e evitando vazamento de recursos.

### Fluxo de autenticação
1. `AuthController.login` delega a `models.Usuario.authenticate` a validação de e-mail/senha com hash `bcrypt`.
2. A classe de modelo emite um JWT assinado com `JWT_SECRET`, retornado ao controller apenas como resultado da regra de negócio.
3. Rotas protegidas usam `@autenticado`, que valida o token, busca o usuário e injeta os dados em `g.current_user`, mantendo a verificação encapsulada.
4. Em caso de falha, um erro customizado `ErroAutenticacao` sinaliza o problema e aciona a lógica de limpeza de sessão.

### Princípios de orientação a objetos aplicados
- **Herança:** `Model` fornece CRUD genérico e é estendido por modelos específicos que adicionam validações e comportamentos próprios.
- **Composição:** `Aluno`, `Personal` e `Gestor` combinam `Usuario` com modelos auxiliares (`_AlunoModel`, `_PersonalModel`, `_GestorModel`) para separar atributos especializados.
- **Abstração:** `ModelBase` define a interface mínima de persistência (create/read/update/delete) e garante consistência entre tabelas.
- **Encapsulamento:** Validações de status, hashing de senha, timestamps e geração de tokens acontecem dentro das classes de domínio, protegendo as regras de acesso externo.

## 🗄️ Banco de dados e migrações
- Banco SQLite localizado em `database/app.db`.
- Migrações versionadas em `database/migrations/*.sql`, cobrindo estruturas como `usuarios`, `gestores`, `personais`, `alunos`, `planos`, `equipamentos`, `fichas` e `exercicios`.
- O script `database/init_db.py` recria o arquivo `app.db` do zero e executa as migrações em ordem numérica. **Atenção:** rodar o script remove o banco existente.

## ⚙️ Configurando o ambiente

### Pré-requisitos
- Python 3.11 ou superior
- `pip`
- (Opcional) `git` para clonar o repositório

### Passo a passo
1. **Clonar o repositório** (ou baixar o código-fonte):
	```powershell
	git clone https://github.com/OtavioSerafim/TP1-APPOO.git
	cd TP1-APPOO
	```

2. **Criar e ativar o ambiente virtual (Windows PowerShell):**
	```powershell
	python -m venv .venv
	.\.venv\Scripts\Activate.ps1
	```

3. **Instalar as dependências:**
	```powershell
	pip install --upgrade pip
	pip install -r requirements.txt
	```

4. **Configurar variáveis de ambiente:** crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
	```env
	FLASK_SECRET_KEY=uma_chave_secreta_qualquer
	JWT_SECRET=outra_chave_muito_secreta
	```
	- `FLASK_SECRET_KEY` garante a integridade das sessões do Flask.
	- `JWT_SECRET` assina os tokens de autenticação.

5. **Criar o banco de dados local:**
	```powershell
	python .\database\init_db.py
	```
	O script gera `database/app.db` aplicando todas as migrações. Rode novamente somente se quiser reiniciar o banco do zero.

6. **Publicar as rotas HTTP (camada Flask):** escolha uma das opções abaixo.
	 - Via Python direto (modo debug ativado em `app.py`):
		 ```powershell
		 python app.py
		 ```
	 - Via CLI do Flask (permite hot reload configurável):
		 ```powershell
		 flask --app app run --debug
		 ```

	 O servidor HTTP estará em [http://127.0.0.1:5000](http://127.0.0.1:5000). Use a rota `/cadastro` para criar o primeiro gestor e liberar o acesso ao restante do backend.

## 🌐 Rotas principais
| Rota | Método | Proteção | Descrição |
|------|--------|----------|-----------|
| `/` | GET | Pública | Tela de login.
| `/cadastro` | GET/POST | Pública | Cadastro de novos usuários (gestor ou personal).
| `/auth/login` | POST | Pública | Endpoint de autenticação (form ou JSON).
| `/auth/logout` | POST | Protegida | Finaliza a sessão apagando o JWT.
| `/personal` | GET | @autenticado | Dashboard do personal trainer.
| `/personal/alunos` | GET | @autenticado | Listagem dos alunos atribuídos ao personal.
| `/personal/fichas` | GET | @autenticado | Consulta fichas de treino relacionadas ao personal.
| `/personal/fichas/novo` | GET/POST | @autenticado | Cadastro de fichas feito pelo personal.
| `/gestor` | GET/POST | @autenticado | Dashboard do gestor com widgets de ocupação e formulários rápidos.
| `/gestor/equipamentos` | GET | @autenticado | Lista equipamentos cadastrados.
| `/gestor/equipamentos/novo` | GET/POST | @autenticado | Criação de equipamentos.
| `/gestor/equipamentos/<int:id>/editar` | POST | @autenticado | Atualiza dados de um equipamento existente.
| `/gestor/equipamentos/<int:id>/remover` | POST | @autenticado | Remove um equipamento.
| `/gestor/planos` | GET | @autenticado | Lista planos disponíveis.
| `/gestor/planos/novo` | GET/POST | @autenticado | Criação de planos.
| `/gestor/planos/<int:id>/editar` | POST | @autenticado | Atualiza detalhes de um plano.
| `/gestor/planos/<int:id>/remover` | POST | @autenticado | Remove um plano.
| `/gestor/alunos` | GET | @autenticado | Painel inicial de alunos.
| `/gestor/alunos/novo` | GET/POST | @autenticado | Cadastro manual de alunos.
| `/gestor/alunos/<int:id>/editar` | POST | @autenticado | Atualiza informações de um aluno.
| `/gestor/alunos/<int:id>/remover` | POST | @autenticado | Remove um aluno da base.
| `/gestor/fichas` | GET | @autenticado | Gestão das fichas criadas para alunos.
| `/gestor/fichas/novo` | GET/POST | @autenticado | Cadastro de fichas pelo gestor.
| `/api/fichas/<int:id>` | GET | @autenticado | Endpoint JSON com detalhes de uma ficha específica.
| `/gestor/entrada` | GET | @autenticado | Tela de autenticação de entrada de alunos.
| `/gestor/entrada/registrar` | POST | @autenticado | Registra a entrada de um aluno e marca presença.
| `/gestor/entrada/saida` | POST | @autenticado | Registra a saída de um aluno, liberando vaga.

> ℹ️ As rotas protegidas também aplicam `@gestor_obrigatorio` ou `@personal_obrigatorio` conforme o perfil, garantindo que cada usuário acesse somente sua área.

## 📦 Dependências principais
- [Flask 3](https://flask.palletsprojects.com/) como camada de interface HTTP e renderização de templates; a lógica de domínio permanece fora das views.
- [PyJWT](https://pyjwt.readthedocs.io/) para emissão e validação de tokens.
- [bcrypt](https://pypi.org/project/bcrypt/) para hash seguro de senhas.
- [python-dotenv](https://pypi.org/project/python-dotenv/) para carregar variáveis de ambiente.

## 🚧 Próximos passos
- Implementar login por reconhecimento facial para Alunos usando OpenCV.

---

Projeto acadêmico desenvolvido pelos alunos Otávio Serafim de Souza Matos e Germano Marques Cipriano Fagundes da disciplina APPOO.