#hecho por Misael Urquidez Arredondo
import mysql.connector

class ciudad_crud:
    def __init__(self, host="localhost", user="root", password="", database="rbe"):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    # CREATE
    def crear(self, clave, nombre):
        try:
            sql = "INSERT INTO ciudad (clave, nombre) VALUES (%s, %s)"
            self.cursor.execute(sql, (clave, nombre))
            self.conn.commit()
            print("CIUDAD REGISTRADA CON ÉXITO")
        except Exception as e:
            print(" Error al crear la ciudad:", e)

    # READ
    def leer(self):
        try:
            sql = "SELECT clave, nombre FROM ciudad"
            self.cursor.execute(sql)
            ciudades = self.cursor.fetchall()

            print("\n--- LISTA DE CIUDADES ---")
            for c in ciudades:
                print(f"Clave: {c[0]} | Nombre: {c[1]}")
            print("-------------------------\n")

            return ciudades
        except Exception as e:
            print("ERROR AL LEER CIUDADES:", e)

    # UPDATE
    def actualizar(self, clave, nuevo_nombre):
        try:
            sql = "UPDATE ciudad SET nombre = %s WHERE clave = %s"
            self.cursor.execute(sql, (nuevo_nombre, clave))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(" Ciudad actualizada correctamente.")
            else:
                print("No se encontró la ciudad.")
        except Exception as e:
            print("error al actualizar ciudad:", e)

    # DELETE
    def eliminar(self, clave):
        try:
            sql = "DELETE FROM ciudad WHERE clave = %s"
            self.cursor.execute(sql, (clave,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(" Ciudad eliminada correctamente.")
            else:
                print(" No se encontró la ciudad.")
        except Exception as e:
            print(" Error al eliminar ciudad:", e)


def main():
    crud = ciudad_crud(password="")  

    while True:
        print("\n===== CRUD CIUDAD =====")
        print("1. Crear ciudad")
        print("2. Leer ciudades")
        print("3. Actualizar ciudad")
        print("4. Eliminar ciudad")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            clave = input("Clave (ej: MTY): ")
            nombre = input("Nombre: ")
            crud.crear(clave, nombre)

        elif opcion == "2":
            crud.leer()

        elif opcion == "3":
            clave = input("Clave de la ciudad a actualizar: ")
            nuevo_nombre = input("Nuevo nombre: ")
            crud.actualizar(clave, nuevo_nombre)

        elif opcion == "4":
            clave = input("Clave a eliminar: ")
            crud.eliminar(clave)

        elif opcion == "5":
            print("Saliendo...")
            break

        else:
            print(" Opción no válida.")


if __name__ == "__main__":
    main()
