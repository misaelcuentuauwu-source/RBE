import mysql.connector

# Configuración de conexión
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

def registrarConductor(registro, nombre, primer_ap, segundo_ap, lic_numero, lic_vencimiento, fecha_contrato):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()
        sql = """
        INSERT INTO conductor (registro, conNombre, conPrimerApell, conSegundoApell, licNumero, licVencimiento, fechaContrato)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(sql, (registro, nombre, primer_ap, segundo_ap, lic_numero, lic_vencimiento, fecha_contrato))
        conexion.commit()
        print("Conductor registrado correctamente.")
        cursor.close()
        conexion.close()

    except mysql.connector.Error as error:
        print(f"Error! al crear conductor: {error}")

def leerConductores():
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM conductor;")
        resultados = cursor.fetchall()

        cursor.close()
        conexion.close()
        return resultados
    except mysql.connector.Error as error:
        print(f"Error al leer conductores: {error}")

def buscarConductor(registro):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM conductor WHERE registro = %s;", (registro,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado
    except mysql.connector.Error as error:
        print(f"Error al buscar conductor: {error}")

def actualizarConductor(registro, nombre, primer_ap, segundo_ap, lic_numero, lic_vencimiento, fecha_contrato):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()
        sql = """
        UPDATE conductor
        SET conNombre=%s,
            conPrimerApell=%s,
            conSegundoApell=%s,
            licNumero=%s,
            licVencimiento=%s,
            fechaContrato=%s
        WHERE registro=%s;
        """
        cursor.execute(sql, (nombre, primer_ap, segundo_ap, lic_numero, lic_vencimiento, fecha_contrato, registro))
        conexion.commit()
        print("Conductor actualizado correctamente.")
        cursor.close()
        conexion.close()

    except mysql.connector.Error as error:
        print(f"Error al actualizar conductor: {error}")

def eliminarConductor(registro):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM conductor WHERE registro = %s;", (registro,))
        conexion.commit()

        print("Conductor eliminado correctamente.")

        cursor.close()
        conexion.close()

    except mysql.connector.Error as error:
        print(f"Error al eliminar conductor: {error}")

registrarConductor(101, "Luis", "Rojas", "Lopez", "LIC12345", "2028-05-01", "2025-11-24")
conductores = leerConductores()
for c in conductores:
    print(f"{c}\n")

print(buscarConductor(101))

actualizarConductor(101, "Luisito", "Rojas", "Lopez", "LIC99999", "2029-01-01", "2025-12-01")

conductores = leerConductores()
for c in conductores:
    print(f"{c}\n")
eliminarConductor(101)

