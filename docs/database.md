# Banco de Dados

> Visão rápida do schema SQLite, migrações e rotinas de manutenção.

## Visão Geral

- Banco local armazenado em `database/app.db`.
- Persistência controlada pelas migrações em `database/migrations/`.
- Script `database/init_db.py` recria o arquivo do zero, aplicando as migrações em ordem numérica.
- As chaves estrangeiras usam regras de `ON DELETE` para manter a consistência entre usuários, perfis e treinos.

## Estrutura das Tabelas

| Tabela | Objetivo | Campos principais |
|--------|----------|-------------------|
| `usuarios` | Dados base de qualquer pessoa autenticada. | `id`, `nome`, `email`, `senha`, `tipo_usuario`, timestamps.
| `alunos` | Extende `usuarios` com informações de treino. | Reutiliza `id` como FK, `personal_id`, `plano_id`, `face_embedding`, `data_ultima_entrada`, `plano_data_inicio`.
| `personais` | Perfil de personal trainer. | `id` (FK de `usuarios`), `data_ultima_atualizacao`.
| `gestores` | Perfil administrativo. | `id` (FK de `usuarios`), `data_ultima_atualizacao`.
| `equipamentos` | Inventário da academia. | `nome`, `valor`, `status`, timestamps.
| `planos` | Planos de assinatura para alunos. | `nome`, `descricao`, `valor_mensal`, `duracao_meses`, timestamps.
| `fichas` | Fichas de treino associadas a aluno e personal. | `aluno_id`, `personal_id`, `descricao`, timestamps.
| `exercicios` | Exercícios listados dentro de uma ficha. | `ficha_id`, `equipamento_id`, `series`, `repeticoes`, `carga`, `tempo_descanso`.

### Relações principais

- `usuarios` é a tabela raiz para `alunos`, `personais` e `gestores` (um-para-um).
- `alunos` pode referenciar um `personal` e um `plano` (opcionais, `ON DELETE SET NULL`).
- `fichas` conectam um `aluno` a um `personal`.
- `exercicios` sempre pertencem a uma `ficha` e podem (opcionalmente) apontar para um `equipamento`.

## Migrações

1. `1_usuarios.sql` — cria a tabela base com validação de `tipo_usuario`.
2. `2_alunos.sql` — adiciona tabela `alunos` com timestamp de última entrada.
3. `3_equipamentos.sql` — catálogo de equipamentos com controle de status.
4. `4_personais.sql` — vincula usuários do tipo personal.
5. `5_alunos_add_personal.sql` — adiciona `personal_id` aos alunos (`ON DELETE SET NULL`).
6. `6_gestores.sql` — vincula usuários do tipo gestor.
7. `7_fichas.sql` — relaciona alunos e personais por ficha de treino.
8. `8_exercicios.sql` — lista exercícios pertencentes às fichas.
9. `9_planos.sql` — cria os planos de assinatura.
10. `10_alunos_add_plano.sql` — adiciona `plano_id` e `plano_data_inicio` aos alunos.

> As migrações são executadas pelo prefixo numérico. Se adicionar uma nova, siga o padrão `{Ultimo Numero + 1}_nome.sql` para manter a ordenação.

---