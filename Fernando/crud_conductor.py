from db_connection import crear_conexion

def crear_conductor(registro, nombre):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conductores (registro, conNombre) VALUES (%s, %s)", (registro, nombre))
    conn.commit()
    print("✅ Conductor creado correctamente")
    conn.close()

def leer_conductores():
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT registro, conNombre FROM conductores")
    for fila in cursor.fetchall():
        print(f"Registro: {fila[0]} | Nombre: {fila[1]}")
    conn.close()

def actualizar_conductor(registro, nuevo_nombre):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("UPDATE conductores SET conNombre = %s WHERE registro = %s", (nuevo_nombre, registro))
    conn.commit()
    print("✏️ Conductor actualizado correctamente")
    conn.close()

def eliminar_conductor(registro):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conductores WHERE registro = %s", (registro,))
    conn.commit()
    print("🗑️ Conductor eliminado correctamente")
    conn.close()
