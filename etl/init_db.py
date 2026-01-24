# etl/init_db.py
import sqlite3
from pathlib import Path

DB_PATH = Path("db/app.db")
SCHEMA_PATH = Path("sql/schema.sql")

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

with sqlite3.connect(DB_PATH) as conn:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(schema)

print(f"DB 초기화 완료: {DB_PATH}")
