import sqlite3

conn = sqlite3.connect("conductores.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS conductores (
        registro INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL
    )
""")
conn.commit()
conn.close()
print("✅ Tabla 'conductores' lista")