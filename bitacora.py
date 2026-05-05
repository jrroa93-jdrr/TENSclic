import sqlite3

def guardar_visita(paciente_id, presion, temp, notas):
    conn = sqlite3.connect("tensclic.db")
    cursor = conn.cursor()
    # Primero hay que crear la tabla si no existe (puedes mover esto a database.py)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            presion TEXT,
            temperatura REAL,
            notas TEXT
        )
    """)
    cursor.execute("INSERT INTO visitas (paciente_id, presion, temperatura, notas) VALUES (?,?,?,?)",
                 (paciente_id, presion, temp, notas))
    conn.commit()
    conn.close()