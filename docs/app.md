# app.py

> Visão resumida do ponto de entrada Flask e das configurações globais.

## Papel do Arquivo

- Inicializa o Flask com pastas customizadas de templates e estáticos (`views/`).
- Carrega variáveis de ambiente via `python-dotenv`.
- Configura `SECRET_KEY` para sessões e mensagens flash.
- Registra rotas apontando para os métodos dos controllers.
- Garante uma instância compartilhada de `Models` por requisição.
- Define tratamento padrão para erros de autenticação.

## Ciclo de Vida da Requisição

1. `@app.before_request` cria `g.models = Models()`, abrindo conexão SQLite.
2. Controller manipula a requisição usando `g.models`.
3. `@app.teardown_request` fecha a conexão após a resposta.

## Rotas Principais

- Autenticação: `/auth/login` (POST), `/auth/logout` (POST).
- Fluxo de login/cadastro: `/`, `/cadastro`.
- Painel do gestor e cadastros: `/gestor`, `/gestor/equipamentos`, `/gestor/planos`, `/gestor/alunos`, etc.

As rotas são adicionadas com `app.add_url_rule`, apontando diretamente para métodos da `UserController` e `AuthController`.

## Tratamento de Erros

- `@app.errorhandler(ErroAutenticacao)` redireciona usuários sem sessão válida para a página de login.
- Remove automaticamente o cookie `auth_token` quando necessário.

## Execução Local

- Ao executar `python app.py`, o Flask inicia em modo debug.
- Certifique-se de definir `FLASK_SECRET_KEY` (e `JWT_SECRET`) no `.env` antes de ligar o servidor.
