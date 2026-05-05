import sqlite3

def agregar_insumo(item, cantidad):
    conn = sqlite3.connect("tensclic.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO insumos (item, cantidad) VALUES (?, ?)", (item, cantidad))
    conn.commit()
    conn.close()

def obtener_stock_bajo(limite=5):
    conn = sqlite3.connect("tensclic.db")
    cursor = conn.cursor()
    cursor.execute("SELECT item, cantidad FROM insumos WHERE cantidad < ?", (limite,))
    alertas = cursor.fetchall()
    conn.close()
    return alertas