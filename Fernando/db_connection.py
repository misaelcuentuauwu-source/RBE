import mysql.connector

def crear_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",       # ← pon tu contraseña si tienes
        database="rbe"     # ← o "prototipo", según tu base
    )