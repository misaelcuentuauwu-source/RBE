import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date

# 🎨 Colores de la marca Rutas Baja Express
COLOR_FONDO = "#f2f2f2"
COLOR_PRINCIPAL = "#0059b3"
COLOR_BOTON = "#ff9900"
COLOR_TEXTO = "#000000"

# 🔌 Conexión a la base de datos
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",      # cambia si usas otro usuario
        password="",      # tu contraseña si tienes una
        database="prototipo"
    )

# 🟦 Función de inicio de sesión
def iniciar_sesion(usuario, contraseña):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM TAQUILLERO WHERE usuario=%s AND contraseña=%s", (usuario, contraseña))
    resultado = cursor.fetchone()

    if resultado:
        messagebox.showinfo("Bienvenido", f"Hola {resultado['taqNombre']} {resultado['taqPrimerApell']} 👋")
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    cursor.close()
    conexion.close()

# 🟧 Función para registrar nuevo taquillero
def registrar_taquillero(nombre, ap1, ap2, usuario, contraseña):
    conexion = conectar()
    cursor = conexion.cursor()
    fecha_contrato = date.today()
    terminal = 1  # fija por ahora

    try:
        cursor.execute("""
            INSERT INTO TAQUILLERO (taqNombre, taqPrimerApell, taqSegundoApell, fechaContrato, usuario, contraseña, terminal)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, ap1, ap2, fecha_contrato, usuario, contraseña, terminal))
        conexion.commit()
        messagebox.showinfo("Éxito", "Taquillero registrado correctamente")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo registrar: {err}")
    finally:
        cursor.close()
        conexion.close()

# 🪟 Interfaz de Login
def ventana_login():
    ventana = tk.Tk()
    ventana.title("Rutas Baja Express - Inicio de Sesión")
    ventana.geometry("400x400")
    ventana.configure(bg=COLOR_FONDO)

    # Logo / título
    tk.Label(ventana, text="Rutas Baja Express", bg=COLOR_PRINCIPAL, fg="white",
             font=("Arial", 18, "bold"), pady=15).pack(fill="x")

    tk.Label(ventana, text="Usuario:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=("Arial", 12)).pack(pady=10)
    usuario_entry = tk.Entry(ventana, width=30)
    usuario_entry.pack()

    tk.Label(ventana, text="Contraseña:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=("Arial", 12)).pack(pady=10)
    contraseña_entry = tk.Entry(ventana, width=30, show="*")
    contraseña_entry.pack()

    def intentar_login():
        usuario = usuario_entry.get()
        contraseña = contraseña_entry.get()
        if usuario and contraseña:
            iniciar_sesion(usuario, contraseña)
        else:
            messagebox.showwarning("Atención", "Por favor, completa todos los campos")

    tk.Button(ventana, text="Iniciar Sesión", bg=COLOR_BOTON, fg="white", font=("Arial", 11, "bold"),
              command=intentar_login).pack(pady=20)

    # Enlace para ir a registro
    tk.Label(ventana, text="¿No tienes cuenta?", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
    tk.Button(ventana, text="Registrar nuevo taquillero", bg=COLOR_PRINCIPAL, fg="white",
              command=lambda: [ventana.destroy(), ventana_registro()]).pack(pady=10)

    ventana.mainloop()

# 🪟 Interfaz de Registro
def ventana_registro():
    ventana = tk.Tk()
    ventana.title("Registro de Taquillero - Rutas Baja Express")
    ventana.geometry("420x520")
    ventana.configure(bg=COLOR_FONDO)

    tk.Label(ventana, text="Registrar Taquillero", bg=COLOR_PRINCIPAL, fg="white",
             font=("Arial", 18, "bold"), pady=15).pack(fill="x")

    campos = ["Nombre", "Primer Apellido", "Segundo Apellido", "Usuario", "Contraseña"]
    entradas = {}

    for campo in campos:
        tk.Label(ventana, text=campo + ":", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=("Arial", 12)).pack(pady=5)
        entrada = tk.Entry(ventana, width=30, show="*" if campo == "Contraseña" else "")
        entrada.pack()
        entradas[campo] = entrada

    def registrar():
        valores = [entradas[c].get() for c in campos]
        if all(valores):
            registrar_taquillero(*valores)
        else:
            messagebox.showwarning("Atención", "Por favor completa todos los campos")

    tk.Button(ventana, text="Registrar", bg=COLOR_BOTON, fg="white", font=("Arial", 11, "bold"),
              command=registrar).pack(pady=20)

    tk.Button(ventana, text="Volver al inicio", bg=COLOR_PRINCIPAL, fg="white",
              command=lambda: [ventana.destroy(), ventana_login()]).pack(pady=10)

    ventana.mainloop()

# 🚀 Ejecutar
if __name__ == "__main__":
    ventana_login()
