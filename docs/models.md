# Documentação dos Models

> Visão rápida das classes de modelo e como trabalhar com elas.

## Visão Geral

O projeto usa **SQLite** e centraliza toda a lógica de persistência na pasta `models/`. As classes seguem um formato em camadas:

- `ModelBase` define a interface CRUD (create/read/update/delete).
- `Model` implementa comportamentos genéricos e hooks (`prepare_create_data`, `prepare_update_data`).
- Modelos específicos (`Usuario`, `Aluno`, `Equipamento` etc.) herdam desses blocos para aplicar regras próprias.
- `Models` é um helper que mantém uma única conexão SQLite e entrega instâncias prontas para uso nas camadas superiores.

## Classes Principais

| Classe          | Tabelas            | Responsabilidades principais |
|-----------------|--------------------|-------------------------------|
| `ModelBase`     | genérica           | Define assinatura CRUD e cursor compartilhado. |
| `Model`         | genérica           | CRUD padrão, montagem de queries e hooks de preparação. |
| `Usuario`       | `usuarios`         | Hash de senha, datas padrão, autenticação JWT. |
| `Aluno`         | `usuarios`, `alunos` | Estende `Usuario`, guarda personal/plano e timestamps extras. |
| `Personal`      | `usuarios`, `personais` | Regras específicas de personal trainer. |
| `Gestor`        | `usuarios`, `gestores`  | Perfil administrativo. |
| `Equipamento`   | `equipamentos`     | Cadastro de equipamentos da academia. |
| `Ficha`         | `fichas`           | Fichas de treino vinculadas a alunos e exercícios. |
| `Exercicio`     | `exercicios`       | Catálogo de exercícios. |
| `Plano`         | `planos`           | Planos de treinamento assinados pelos alunos. |
| `Models`        | múltiplas          | Singleton simples para compartilhar conexão via propriedades. |

## Fluxos Essenciais

### Criar um aluno

1. Preencha os dados básicos do usuário (`nome`, `email`, `senha`).
2. Inclua dados opcionais específicos (`personal_id`, `plano_id`, `face_embedding` etc.).
3. Chame `Models().aluno.create(payload)`. O método cria o registro em `usuarios`, depois sincroniza a linha correspondente na tabela `alunos`.

### Autenticar um usuário

1. Garanta que a variável de ambiente `JWT_SECRET` esteja definida.
2. Chame `Models().usuario.authenticate(email, senha)`.
3. O método valida o hash armazenado, monta o payload e devolve um token JWT com validade de 24 horas.

## Erros e Convenções

- `ErroDadosInvalidos`: lançado quando dados obrigatórios estão ausentes ou vazios (por exemplo, senha na criação de usuários).
- `ErroAutenticacao`: disparado em credenciais inválidas durante o login.
- `ErroConfiguracao`: indica ausência de variáveis obrigatórias (caso do `JWT_SECRET`).
- Sempre que sobrescrever `prepare_create_data` ou `prepare_update_data`, mantenha o retorno como um dicionário pronto para o SQL.

## Como Extender

1. Crie uma nova classe herdando de `Model` (ou de um modelo existente) e configure `table_name`, `columns` e chaves conforme necessário.
2. Ajuste os hooks `prepare_*` para validar e preencher valores padrão da nova tabela.
3. Registre a classe na fábrica `Models` em `models/main.py` para acessá-la via propriedades (ex.: `models.novo_modelo`).
4. Atualize a tabela acima e, se aplicável, adicione uma migration na pasta `database/migrations/`.

---