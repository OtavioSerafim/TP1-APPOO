# Decorators

> Referência rápida dos decoradores utilitários disponíveis em `utils/decorators/`.

## `autenticado`

- **Objetivo**: proteger rotas Flask exigindo um token JWT válido no cookie `auth_token`.
- **Como funciona**:
  1. Busca o token em `request.cookies`.
  2. Valida assinatura e expiração usando `JWT_SECRET`.
  3. Carrega o usuário correspondente via `g.models.usuario`.
  4. Em caso de falha, lança `ErroAutenticacao` e indica para limpar o cookie.
- **Contexto**: adiciona `g.current_user` e `g.current_user_claims` para uso pela view.

## Uso típico

```python
from utils.decorators.Autenticado import autenticado

@app.route('/area-restrita')
@autenticado
def area_restrita():
    return render_template('restrita.html', usuario=g.current_user)
```