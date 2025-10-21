CREATE TABLE IF NOT EXISTS fichas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    personal_id INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    criado_em TEXT NOT NULL DEFAULT (datetime('now')),
    atualizado_em TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE,
    FOREIGN KEY (personal_id) REFERENCES personais(id) ON DELETE CASCADE
);
