from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "app.db"
MIGRATIONS_DIR = BASE_DIR / "migrations"

if DB_PATH.exists():
    DB_PATH.unlink()

with sqlite3.connect(DB_PATH) as conn:
    for sql_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
        conn.executescript(sql_file.read_text(encoding="utf-8"))


print(f"Banco criado em {DB_PATH}")
