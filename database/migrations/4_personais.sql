CREATE TABLE IF NOT EXISTS personais (
	id INTEGER PRIMARY KEY,
	data_ultima_atualizacao TEXT NOT NULL DEFAULT (datetime('now')),
	FOREIGN KEY (id) REFERENCES usuarios(id) ON DELETE CASCADE
);
