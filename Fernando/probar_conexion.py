from conexion import crear_conexion

def mostrar_terminales():
    try:
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, telefono, dirCalle, dirColonia FROM terminal")
        terminales = cursor.fetchall()
        print("🏁 Terminales registradas:")
        for t in terminales:
            print(f"{t[0]} | Tel: {t[1]} | Dirección: {t[2]}, {t[3]}")
        conn.close()
    except Exception as e:
        print("❌ Error en la conexión:", e)

mostrar_terminales()