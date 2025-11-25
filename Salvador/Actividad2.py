import mysql.connector

configuracion = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'rbe',
    'charset': 'utf8mb4',
    'connect_timeout': 10
}

def obtenerConexion():
    return mysql.connector.connect(**configuracion)


def registrarPasajero(nombre, primer_ap, segundo_ap, fecha_nac, edad):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO pasajero (paNombre, paPrimerApell, paSegundoApell, fechaNacimiento, edad)
        VALUES (%s, %s, %s, %s, %s);
        """

        cursor.execute(sql, (nombre, primer_ap, segundo_ap, fecha_nac, edad))
        conexion.commit()

        print("Pasajero registrado correctamente.")

        cursor.close()
        conexion.close()

    except mysql.connector.Error as error:
        print(f"Error al crear pasajero: {error}")


def leerPasajeros():
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM pasajero;")
        resultados = cursor.fetchall()

        cursor.close()
        conexion.close()
        return resultados

    except mysql.connector.Error as error:
        print(f"Error al leer pasajeros: {error}")


def buscarPasajero(id_pasajero):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM pasajero WHERE num = %s;", (id_pasajero,))
        resultado = cursor.fetchone()

        cursor.close()
        conexion.close()
        return resultado

    except mysql.connector.Error as error:
        print(f"Error al buscar pasajero: {error}")


def actualizarPasajero(id_pasajero, nombre, primer_ap, segundo_ap, fecha_nac, edad):
    try:
        conexion = obtenerConexion()
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

        print("Padajero actualizado correctamente.")

        cursor.close()
        conexion.close()

    except mysql.connector.Error as error:
        print(f"Error al actualizar pasajero: {error}")


def eliminarPasajero(id_pasajero):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM pasajero WHERE num = %s;", (id_pasajero,))
        conexion.commit()

        print("✔ Pasajero eliminado correctamente.")

        cursor.close()
        conexion.close()

    except mysql.connector.Error as error:
        print(f"Error al eliminar pasajero: {error}")


registrarPasajero("Garcia", "Bojorquez", "Salvador", "2006-02-17", 19)

pasajeros = leerPasajeros()
for p in pasajeros:
    print(f"{p}\n")

print(buscarPasajero(1))

actualizarPasajero(1, "Urquidez", "Arredondo", "Misael", "2006-03-08", 19)

pasajeros = leerPasajeros()
for p in pasajeros:
    print(f"{p}\n")
