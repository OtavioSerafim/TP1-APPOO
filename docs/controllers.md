# Controllers

> Resumo da camada responsável por orquestrar requisições HTTP e acionar os models.

## Organização

- Arquivos armazenados em `controller/`.
- Cada controlador agrupa rotas relacionadas a um tema (autenticação, usuários, cadastros).
- Utilizam o objeto `g.models` para acessar os models e delegar regras de negócio.

```
controller/
├── auth_controller.py
├── equipment_controller.py
├── plan_controller.py
├── student_controller.py
└── user_controller.py
```

## Principais Responsabilidades

- Receber dados dos formulários ou JSON (`request.form`, `request.get_json`) e normalizar entradas.
- Validar campos obrigatórios e retornar mensagens amigáveis via `flash` (HTML) ou `jsonify` (API).
- Chamar métodos dos models (`create`, `authenticate`, `update`, `delete`, `get_all`) e encapsular erros de negócio.
- Decidir a resposta adequada com `render_template`, `jsonify` ou redirecionar (`redirect`, `url_for`).
- Decorar rotas privadas com `@autenticado` e `@gestor_obrigatorio` para reforçar autorização.

## Fluxo Geral de uma Requisição

1. Controller recebe a requisição HTTP.
2. Extrai, normaliza e valida os dados do formulário/corpo.
3. Aciona o model correspondente (ex.: `g.models.usuario.authenticate`, `g.models.equipamento.update`).
4. Lida com erros (`ErroDadosInvalidos`, `ErroAutenticacao`, `ErroConfiguracao`), convertendo em respostas apropriadas e com feedback consistente.
5. Renderiza template, retorna JSON ou redireciona com mensagens `flash` persistidas na sessão.

## Convenções

- Métodos definidos como `@staticmethod` para evitar instâncias e simplificar testes.
- Rotas seguem a nomenclatura da função (ex.: `login`, `equipamentos`, `cadastro_plano`).
- `flash` comunica feedback em rotas HTML; `jsonify` e `make_response` encapsulam respostas REST.
- Exceções específicas (`ErroDadosInvalidos`, `ErroAutenticacao`) devem ser capturadas e convertidas em mensagens amigáveis.
- A lógica de negócio permanece nos models; controllers orquestram fluxo HTTP, autorização e feedback.
