import sqlite3

def inicializar_db():
    conn = sqlite3.connect("tensclic.db")
    cursor = conn.cursor()
    # Tabla TENS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            rut TEXT NOT NULL UNIQUE,
            registro_sis TEXT NOT NULL UNIQUE,
            especialidad TEXT NOT NULL
        )
    """)
    # Tabla PACIENTES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            direccion TEXT NOT NULL,
            peso REAL,
            estatura REAL,
            patologias TEXT,
            medicamentos TEXT,
            requiere_insumos BOOLEAN
        )
    """)
    # Tabla INSUMOS (LogiPy)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insumos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            cantidad INTEGER
        )
    """)
    conn.commit()
    conn.close()