CREATE TABLE IF NOT EXISTS alunos (
	id INTEGER PRIMARY KEY,
	face_embedding TEXT,
	data_ultima_entrada TEXT NOT NULL DEFAULT (datetime('now')),
	FOREIGN KEY (id) REFERENCES usuarios(id) ON DELETE CASCADE
);
