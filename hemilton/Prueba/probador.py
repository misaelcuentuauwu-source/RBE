# main.py
from conexion import crear_conexion

try:
    conexion = crear_conexion()
    print("Conexión exitosa a la base de datos.")

except Exception as e:
    print("Error de conexión:", e)
