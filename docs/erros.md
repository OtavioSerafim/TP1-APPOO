# Erros Personalizados

> Visão rápida sobre as exceções definidas em `utils/errors/` e como tratá-las nas camadas superiores.

## Visão Geral

- Todas as exceções herdam de `ErroBase`, que encapsula uma mensagem legível.
- Os modelos levantam erros específicos para sinalizar problemas de dados, autenticação ou configuração.
- Controllers e decorators devem capturar essas exceções para responder ao usuário com mensagens claras (flash, JSON ou página amigável).

## Hierarquia

```
ErroBase
├── ErroAutenticacao
├── ErroConfiguracao
└── ErroDadosInvalidos
```

## Catálogo de Erros

| Classe | Quando ocorre | Ações recomendadas |
|--------|----------------|--------------------|
| `ErroAutenticacao` | Credenciais inválidas, token inexistente ou sessão expirada. | Limpar sessão, redirecionar para login e exibir mensagem "Email ou senha inválidos". Retornar HTTP 401 em APIs. |
| `ErroConfiguracao` | Falta de variáveis de ambiente (`JWT_SECRET`, `FLASK_SECRET_KEY`) ou ajustes obrigatórios. | Registrar log, abortar inicialização ou responder com HTTP 500 indicando erro interno. |
| `ErroDadosInvalidos` | Dados obrigatórios ausentes (ex.: senha vazia) ou payload inconsistente. | Exibir mensagem orientativa ao usuário, marcar campos inválidos e retornar HTTP 400 em APIs. |

## Pontos de Uso

- `models.Usuario.authenticate` lança `ErroAutenticacao` quando e-mail/senha não conferem ou quando o segredo JWT está ausente (`ErroConfiguracao`).
- Operações CRUD em `models.Model` e derivados podem levantar `ErroDadosInvalidos` quando `prepare_create_data` ou `prepare_update_data` retornam payload vazio.
- Decoradores de autenticação (`utils.decorators.Autenticado`) podem transformar `ErroAutenticacao` em redirecionamentos com mensagens flash.

## Exemplo de Uso em Controller

```python
from utils.errors.erroDadosInvalidos import ErroDadosInvalidos

try:
    models.usuario.create(form_data)
    flash("Usuário cadastrado com sucesso!", "success")
except ErroDadosInvalidos as erro:
    flash(str(erro), "error")
```

---