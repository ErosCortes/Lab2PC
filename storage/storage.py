"""Crea la base de datos SQLite e inserta los dataframes CSV generados."""
import sqlite3
import pandas as pd
from pathlib import Path
from config.config import DB_PATH

SCHEMA = """
BEGIN;
CREATE TABLE IF NOT EXISTS hosts (
    id INTEGER PRIMARY KEY,
    hostname TEXT NOT NULL UNIQUE,
    os TEXT NOT NULL,
    environment TEXT NOT NULL,
    country TEXT NOT NULL,
    node TEXT
);
CREATE TABLE IF NOT EXISTS logs (
    id_log INTEGER PRIMARY KEY,
    id_server INTEGER NOT NULL,
    timestamp TEXT,
    request_type TEXT,
    response_time_ms INTEGER,
    status_code INTEGER,
    user TEXT,
    FOREIGN KEY (id_server) REFERENCES hosts(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS maintenance (
    id_maintenance INTEGER PRIMARY KEY,
    id_server INTEGER NOT NULL,
    date TEXT,
    type TEXT,
    duration_min INTEGER,
    technician TEXT,
    notes TEXT,
    FOREIGN KEY (id_server) REFERENCES hosts(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
COMMIT;
"""

def create_db(db_path=DB_PATH):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"Base de datos creada en {db_path}")

def insert_from_csv(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    for name in ('hosts', 'logs', 'maintenance'):
        path = f'data/{name}.csv'
        try:
            df = pd.read_csv(path)
            # Si la tabla está vacía insertamos; si ya tiene datos, append (avoid duplicates is left to user)
            df.to_sql(name, conn, if_exists='append', index=False)
            print(f'Insertado {name} -> {len(df)} filas')
        except FileNotFoundError:
            print(f'Archivo faltante: {path}')
    conn.close()

if __name__ == '__main__':
    create_db()
    insert_from_csv()
