# Controllers

> Resumo da camada responsável por orquestrar requisições HTTP e acionar os models.

## Organização

- Arquivos armazenados em `controller/`.
- Cada controlador agrupa rotas relacionadas a um tema (autenticação, usuários, cadastros).
- Utilizam o objeto `g.models` para acessar os models e delegar regras de negócio.

```
controller/
├── auth_controller.py
└── user_controller.py
```

## Principais Responsabilidades

- Receber dados dos formulários ou JSON (`request.form`, `request.get_json`).
- Validar campos obrigatórios e retornar mensagens amigáveis via `flash` ou `jsonify`.
- Chamar métodos dos models (`create`, `authenticate`, `get_all`) e tratar exceções.
- Escolher a view adequada com `render_template` ou redirecionar (`redirect`, `url_for`).
- Envolver rotas privadas com o decorator `@autenticado` para exigir token válido.

## Fluxo Geral de uma Requisição

1. Controller recebe a requisição HTTP.
2. Extrai e valida os dados do formulário/corpo.
3. Aciona o model correspondente (ex.: `g.models.usuario.authenticate`).
4. Lida com erros (`ErroDadosInvalidos`, `ErroAutenticacao`), convertendo em respostas apropriadas.
5. Renderiza template ou retorna JSON com o resultado.

## Convenções

- Métodos definidos como `@staticmethod` para evitar instâncias.
- Nomenclatura de rotas segue o nome da função (ex.: `login`, `gestor`, `cadastro_plano`).
- Utilize `flash` para feedback em páginas HTML e `jsonify` para respostas de APIs.
- Mantenha a lógica de negócio nos models; controllers focam em fluxo HTTP.
