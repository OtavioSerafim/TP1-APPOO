# Decorators

> Referência rápida dos decoradores utilitários disponíveis em `utils/decorators/`.

## `autenticado`

- **Objetivo**: proteger rotas Flask exigindo um token JWT válido no cookie `auth_token`.
- **Como funciona**:
  1. Busca o token em `request.cookies`.
  2. Valida assinatura e expiração usando `JWT_SECRET`.
  3. Carrega o usuário correspondente via `g.models.usuario`.
  4. Em caso de falha, define `g.auth_error_clear_cookie` para que o cookie seja limpo e lança `ErroAutenticacao`.
- **Contexto**: adiciona `g.current_user` e `g.current_user_claims` para uso pela view.

## `gestor_obrigatorio`

- **Objetivo**: restringir rotas a usuários autenticados do tipo `gestor`.
- **Pré-requisito**: deve ser aplicado após `@autenticado`, garantindo que `g.current_user` esteja preenchido.
- **Validação**: verifica o campo `tipo_usuario` do usuário carregado; dispara `ErroAutenticacao` se o tipo não for `gestor`.
- **Comportamento**: mantém o fluxo original da view quando a verificação passa, permitindo uso em conjunto com `flash` ou respostas JSON.

## `personal_obrigatorio`

- **Objetivo**: restringir rotas a usuários autenticados do tipo `personal`.
- **Pré-requisito**: deve suceder `@autenticado` para garantir que o contexto `g.current_user` esteja populado.
- **Validação**: lê `tipo_usuario` do usuário e levanta `ErroAutenticacao` quando não corresponder a `personal`.
- **Uso típico**: aplicado em rotas de acompanhamento de alunos ou fichas específicas de personal trainers.

## Uso típico

```python
from utils.decorators.Autenticado import autenticado
from utils.decorators.TipoUsuario import gestor_obrigatorio, personal_obrigatorio

@app.route('/area-restrita')
@autenticado
def area_restrita():
    return render_template('restrita.html', usuario=g.current_user)

@app.route('/gestor/equipamentos', methods=['POST'])
@autenticado
@gestor_obrigatorio
def atualizar_equipamento():
    ...

@app.route('/personal/fichas')
@autenticado
@personal_obrigatorio
def fichas_personal():
    ...
```