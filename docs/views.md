# Views

> Visão geral da camada de apresentação: templates, estilos e scripts.

## Organização

- Pasta `views/templates/`: arquivos HTML (Jinja2) que renderizam as telas.
- Pasta `views/static/`: estilos CSS e scripts JavaScript servidos pelo Flask.
- `views/static/general.css`: estilos compartilhados entre páginas.
- Subpasta `views/static/scripts/`: scripts utilitários (ex.: alertas e logout).

```
views/
├── templates/
│   ├── login.html
│   ├── cadastro.html
│   ├── ...
│
└── static/
    ├── general.css
    ├── login.css
    ├── ...
    └── scripts/
        ├── flash-message.js
        └── processa-logout.js
```

## Fluxo de Renderização

1. Controllers preparam os dados (ex.: lista de planos) e chamam `render_template`.
2. Os templates Jinja2 consomem variáveis de contexto (`{{ }}`) e percorrem listas com `{% for %}`.
3. Layouts referenciam os arquivos CSS/JS via `url_for('static', filename='...')`.
4. Scripts opcionais lidam com feedback visual (flash) e ações como logout.

## Conjuntos de Telas

- **Autenticação**: `login.html`, `cadastro.html`.
- **Gestor**: dashboards e cadastros (`home-gestor.html`, `equipamentos.html`, `planos.html`).
- **Alunos/Personais**: telas específicas (`alunos-gestor.html`, `home-personal.html`).
- **Fluxo de entrada**: `autentica-entrada.html` para registro de passagem.

> As telas compartilham classes CSS nomeadas de forma consistente com arquivos dedicados (`home-gestor.css`, `planos.css`, etc.).

## Scripts Disponíveis

| Arquivo | Função |
|---------|--------|
| `flash-message.js` | Exibe e oculta mensagens flash com transições suaves. |
| `processa-logout.js` | Intercepta o botão de logout, chama a rota `/auth/logout` e redireciona ao login. |