# Views

> Visão geral da camada de apresentação: templates, estilos e scripts.

## Organização

- Pasta `views/templates/`: arquivos HTML (Jinja2) que renderizam as telas e consomem variáveis do contexto Flask.
- Pasta `views/static/`: estilos CSS e scripts JavaScript servidos pelo Flask.
- `views/static/general.css`: estilos compartilhados entre páginas.
- Folhas específicas por domínio (`home-gestor.css`, `planos.css`, `cadastro.css`, etc.).
- Subpasta `views/static/scripts/`: scripts utilitários (ex.: alertas, duplicação de exercícios e logout).

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
        ├── processa-logout.js
        ├── alunos.js
        ├── equipamentos.js
        ├── planos.js
        ├── ficha-popup.js
        └── duplica-exercicio.js
```

## Fluxo de Renderização

1. Controllers preparam os dados (ex.: lista de planos ou alunos) e chamam `render_template`.
2. Os templates Jinja2 consomem variáveis de contexto (`{{ }}`) e percorrem listas com `{% for %}`.
3. O *context processor* `inject_academia_status` adiciona dados de ocupação (`alunos_na_academia`, `capacidade_maxima_academia`) disponíveis em todas as páginas.
4. Layouts referenciam os arquivos CSS/JS via `url_for('static', filename='...')`.
5. Scripts opcionais lidam com feedback visual (flash), duplicação de exercícios, filtros de listagem e ações como logout.

## Conjuntos de Telas

- **Autenticação**: `login.html`, `cadastro.html`.
- **Gestor**: dashboards e cadastros (`home-gestor.html`, `equipamentos.html`, `planos.html`, `fichas-gestor.html`).
- **Alunos/Personais**: telas específicas (`alunos-gestor.html`, `alunos-personal.html`, `home-personal.html`, `fichas-personal.html`).
- **Fluxo de entrada**: `autentica-entrada.html` para registro de passagem.
- **Formulários auxiliares**: `cadastro-ficha-gestor.html`, `cadastro-ficha-personal.html`, `cadastro-equipamento.html`, `cadastro-aluno.html`.

> As telas compartilham classes CSS nomeadas de forma consistente com arquivos dedicados (`home-gestor.css`, `planos.css`, etc.).

## Scripts Disponíveis

| Arquivo | Função |
|---------|--------|
| `flash-message.js` | Exibe e oculta mensagens flash com transições suaves. |
| `processa-logout.js` | Intercepta o botão de logout, chama a rota `/auth/logout` e redireciona ao login. |
| `alunos.js` | Aplica filtros e atualiza a listagem de alunos exibida nas telas de gestão/personal. |
| `equipamentos.js` | Dispara submits das ações de edição/remoção diretamente das tabelas de equipamentos. |
| `planos.js` | Controla aberturas de modal e sincroniza dados nos formulários de planos. |
| `ficha-popup.js` | Exibe detalhes das fichas em pop-ups sem recarregar a página. |
| `duplica-exercicio.js` | Duplica blocos de exercícios dinamicamente nos formulários de ficha. |