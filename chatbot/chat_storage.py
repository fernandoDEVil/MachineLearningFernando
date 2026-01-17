import sqlite3
from datetime import datetime

DB_NAME = "chat_history.db"


# -------------------------------------------------
# Inicializar base de datos
# -------------------------------------------------
def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rol TEXT NOT NULL,
            contenido TEXT NOT NULL,
            fecha TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# -------------------------------------------------
# Guardar mensaje
# -------------------------------------------------
def guardar_mensaje(rol, contenido):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO mensajes (rol, contenido, fecha)
        VALUES (?, ?, ?)
    """, (
        rol,
        contenido,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


# -------------------------------------------------
# Obtener lista de conversaciones (por fecha)
# -------------------------------------------------
def obtener_conversaciones():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT substr(fecha, 1, 10) AS fecha
        FROM mensajes
        ORDER BY fecha DESC
    """)

    conversaciones = [fila[0] for fila in cursor.fetchall()]
    conn.close()
    return conversaciones


# -------------------------------------------------
# Obtener mensajes de una conversación (fecha)
# -------------------------------------------------
def obtener_mensajes_por_fecha(fecha):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT rol, contenido
        FROM mensajes
        WHERE substr(fecha, 1, 10) = ?
        ORDER BY fecha ASC
    """, (fecha,))

    mensajes = cursor.fetchall()
    conn.close()
    return mensajes


# -------------------------------------------------
# (Opcional futuro) Borrar historial completo
# -------------------------------------------------
def borrar_historial():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mensajes")
    conn.commit()
    conn.close()
