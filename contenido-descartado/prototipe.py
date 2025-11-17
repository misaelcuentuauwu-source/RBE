import mysql.connector
from datetime import date

# Conexión a la base de datos
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # Cambia si tienes otra cuenta
        password="",         # Cambia si tu MySQL tiene contraseña
        database="prototipo"
    )

# Función para iniciar sesión
def iniciar_sesion():
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM TAQUILLERO WHERE usuario=%s AND contraseña=%s", (usuario, contraseña))
    resultado = cursor.fetchone()

    if resultado:
        print(f"\n Bienvenido {resultado['taqNombre']} {resultado['taqPrimerApell']}!\n")
    else:
        print("\n Usuario o contraseña incorrectos.\n")

    cursor.close()
    conexion.close()

# Función para registrar un nuevo taquillero
def registrar_taquillero():
    nombre = input("Nombre: ")
    primer_apellido = input("Primer apellido: ")
    segundo_apellido = input("Segundo apellido: ")
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    conexion = conectar()
    cursor = conexion.cursor()

    # Asumimos que todos pertenecen a la terminal 1 por ahora
    fecha_contrato = date.today()
    terminal = 1

    try:
        cursor.execute("""
            INSERT INTO TAQUILLERO (taqNombre, taqPrimerApell, taqSegundoApell, fechaContrato, usuario, contraseña, terminal)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, primer_apellido, segundo_apellido, fecha_contrato, usuario, contraseña, terminal))
        
        conexion.commit()
        print("\n Taquillero registrado correctamente.\n")
    except mysql.connector.Error as err:
        print(f"\n Error al registrar: {err}\n")
    finally:
        cursor.close()
        conexion.close()

# Menú principal
def menu():
    while True:
        print("===== MENÚ PRINCIPAL =====")
        print("1. Iniciar sesión")
        print("2. Registrar nuevo taquillero")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            iniciar_sesion()
        elif opcion == "2":
            registrar_taquillero()
        elif opcion == "3":
            print(" Saliendo del sistema...")
            break
        else:
            print(" Opción no válida.\n")

# Ejecutar el menú
if __name__ == "__main__":
    menu()
