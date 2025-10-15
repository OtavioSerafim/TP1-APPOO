CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo_usuario TEXT NOT NULL,
    criado_em TEXT NOT NULL DEFAULT (DATE('now')),
    atualizado_em TEXT NOT NULL DEFAULT (DATE('now')),
);