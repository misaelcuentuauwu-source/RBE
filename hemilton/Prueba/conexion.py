# db_connection.py
# -------------------------------------
# Archivo dedicado únicamente a la conexión a MySQL
# -------------------------------------

import mysql.connector

def crear_conexion():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="rbe"
    )
