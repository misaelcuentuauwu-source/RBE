import mysql.connector

# ------------------------------
# CONEXIÓN BASE
# ------------------------------
configuracion = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'rbe',
    'charset': 'utf8mb4',
    'connect_timeout': 10
}

def obtener_conexion():
    return mysql.connector.connect(**configuracion)

# ------------------------------
# CREAR REGISTRO
# ------------------------------
def crear_pasajero(nombre, primer_ap, segundo_ap, fecha_nac, edad):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO pasajero (paNombre, paPrimerApell, paSegundoApell, fechaNacimiento, edad)
        VALUES (%s, %s, %s, %s, %s);
        """

        cursor.execute(sql, (nombre, primer_ap, segundo_ap, fecha_nac, edad))
        conexion.commit()

        print("✔ Pasajero registrado correctamente.")

        cursor.close()
        conexion.close()

    except mysql.connector.Error as error:
        print(f"❌ Error al crear pasajero: {error}")


# ------------------------------
# LEER TODOS LOS REGISTROS
# ------------------------------
def leer_pasajeros():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM pasajero;")
        resultados = cursor.fetchall()

        cursor.close()
        conexion.close()
        return resultados

    except mysql.connector.Error as error:
        print(f"❌ Error al leer pasajeros: {error}")


# ------------------------------
# LEER PASAJERO POR ID
# ------------------------------
def leer_pasajero_por_id(id_pasajero):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM pasajero WHERE num = %s;", (id_pasajero,))
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()
        return resultado

    except mysql.connector.Error as error:
        print(f"❌ Error al buscar pasajero: {error}")


# ------------------------------
# ACTUALIZAR REGISTRO
# ------------------------------
def actualizar_pasajero(id_pasajero, nombre, primer_ap, segundo_ap, fecha_nac, edad):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE pasajero
        SET paNombre=%s,
            paPrimerApell=%s,
            paSegundoApell=%s,
            fechaNacimiento=%s,
            edad=%s
        WHERE num=%s;
        """

        cursor.execute(sql, (nombre, primer_ap, segundo_ap, fecha_nac, edad, id_pasajero))
        conexion.commit()

        print("✔ Pasajero actualizado correctamente.")

        cursor.close()
        conexion.close()

    except mysql.connector.Error as error:
        print(f"❌ Error al actualizar pasajero: {error}")


# ------------------------------
# ELIMINAR REGISTRO
# ------------------------------
def eliminar_pasajero(id_pasajero):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM pasajero WHERE num = %s;", (id_pasajero,))
        conexion.commit()

        print("✔ Pasajero eliminado correctamente.")

        cursor.close()
        conexion.close()

    except mysql.connector.Error as error:
        print(f"❌ Error al eliminar pasajero: {error}")


# ------------------------------
# EJEMPLOS DE USO (DESCOMENTA)
# ------------------------------

# crear_pasajero("Carlos", "Lopez", "Ramirez", "1999-05-10", 25)

# pasajeros = leer_pasajeros()
# for p in pasajeros:
#     print(p)

# print(leer_pasajero_por_id(1))

# actualizar_pasajero(1, "Carlos", "Lopez", "Hernandez", "1999-05-10", 25)

# eliminar_pasajero(3)
