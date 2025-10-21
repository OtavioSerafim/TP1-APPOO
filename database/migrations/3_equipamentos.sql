CREATE TABLE IF NOT EXISTS equipamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    valor REAL NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('disponivel', 'quebrada', 'no_conserto')),
    criado_em TEXT NOT NULL DEFAULT (DATE('now')),
    atualizado_em TEXT NOT NULL DEFAULT (DATE('now'))
);
