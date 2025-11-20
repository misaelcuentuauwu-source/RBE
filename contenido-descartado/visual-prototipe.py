#!/usr/bin/env python3
# app_taquilleros_pyside6.py
# Sistema: login y registro de taquilleros con PySide6 + diseño importado del .ui
# Autor: adaptado para Misael

import sys
from datetime import date
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFrame, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt

# ---------------------------
# Conexión a la base de datos
# ---------------------------
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="prototipo",
        auth_plugin="mysql_native_password"
    )

def iniciar_sesion_bd(usuario, contrasena):
    try:
        cn = conectar()
        cur = cn.cursor(dictionary=True)
        cur.execute("SELECT * FROM taquillero WHERE usuario=%s AND contrasena=%s", (usuario, contrasena))
        row = cur.fetchone()
        cur.close()
        cn.close()
        return row
    except mysql.connector.Error as e:
        QMessageBox.critical(None, "Error BD", f"Error al conectar: {e}")
        return None

def registrar_taquillero_bd(nombre, ap1, ap2, usuario, contrasena, terminal=1):
    try:
        cn = conectar()
        cur = cn.cursor()
        fecha_contrato = date.today()
        cur.execute("""
            INSERT INTO taquillero (taqnombre, taqprimerapell, taqsegundoapell, fechacontrato, usuario, contrasena, terminal)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, ap1, ap2, fecha_contrato, usuario, contrasena, terminal))
        cn.commit()
        cur.close()
        cn.close()
        return True, None
    except mysql.connector.Error as e:
        return False, str(e)

# ---------------------------
# Interfaz principal
# ---------------------------
class App:
    def __init__(self):
        self.usuario_actual = None
        self.app = QApplication(sys.argv)
        self.ventana_login()
        sys.exit(self.app.exec())

    # --------- ventana login ----------
    def ventana_login(self):
        self.win_login = QWidget()
        self.win_login.setWindowTitle("Rutas Baja Express - Inicio de Sesión")
        self.win_login.setGeometry(100, 100, 480, 500)

        # Fondo degradado
        self.win_login.setStyleSheet("""
        QWidget {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                              stop:0 #1181c3, stop:1 #ed7237);
            font-family: 'Segoe UI';
            color: #000000;
        }
        QLineEdit {
            background-color: #ffffff;
            border: 2px solid #1181c3;
            border-radius: 10px;
            padding: 8px;
            font-size: 11pt;
        }
        QPushButton {
            background-color: #ed7237;
            border-radius: 10px;
            color: white;
            font-weight: bold;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #f28c50;
        }
        QLabel {
            color: #000000;
            font-size: 10.5pt;
        }
        """)

        # Layout principal
        layout_main = QVBoxLayout(self.win_login)
        layout_main.setAlignment(Qt.AlignCenter)

        # Espaciador superior
        layout_main.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # --- marco central estilo tarjeta ---
        frame = QFrame()
        frame.setMaximumSize(400, 360)
        frame.setStyleSheet("""
        QFrame {
            background-color: #f2f2f2;
            border-radius: 20px;
            border: 3px solid #ffffff;
        }
        """)

        layout_card = QVBoxLayout(frame)

        titulo = QLabel("Rutas Baja Express")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #1181c3; font-size: 20pt; font-weight: bold; margin-bottom: 10px;")
        layout_card.addWidget(titulo)

        subtitulo = QLabel("Inicio de Sesión")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("color: #ed7237; font-size: 12pt; font-weight: bold;")
        layout_card.addWidget(subtitulo)

        layout_card.addSpacing(10)

        # Campos
        lbl_user = QLabel("Usuario")
        layout_card.addWidget(lbl_user)
        self.usuario_entry = QLineEdit()
        self.usuario_entry.setPlaceholderText("Ingresa tu usuario...")
        layout_card.addWidget(self.usuario_entry)

        lbl_pass = QLabel("Contraseña")
        layout_card.addWidget(lbl_pass)
        self.contrasena_entry = QLineEdit()
        self.contrasena_entry.setEchoMode(QLineEdit.Password)
        self.contrasena_entry.setPlaceholderText("•••••••••••")
        layout_card.addWidget(self.contrasena_entry)

        layout_card.addSpacing(10)

        # Botones
        btn_login = QPushButton("Iniciar Sesión")
        btn_login.clicked.connect(self.intentar_login)
        layout_card.addWidget(btn_login)

        btn_registrar = QPushButton("Registrar nuevo taquillero")
        btn_registrar.setStyleSheet("""
        QPushButton {
            background-color: #1181c3;
            color: white;
            border-radius: 10px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #0d6ca4;
        }
        """)
        btn_registrar.clicked.connect(self.abrir_registro_taquillero)
        layout_card.addWidget(btn_registrar)

        layout_main.addWidget(frame)

        # Espaciador inferior
        layout_main.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Footer
        footer = QLabel("© 2025 Rutas Baja Express")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: white; font-size: 9pt;")
        layout_main.addWidget(footer)

        self.win_login.show()

    def intentar_login(self):
        usuario = self.usuario_entry.text().strip()
        contrasena = self.contrasena_entry.text().strip()
        if not usuario or not contrasena:
            QMessageBox.warning(self.win_login, "Atención", "Completa todos los campos")
            return
        fila = iniciar_sesion_bd(usuario, contrasena)
        if fila:
            self.usuario_actual = fila
            QMessageBox.information(self.win_login, "Bienvenido", f"Hola {fila.get('taqnombre')} {fila.get('taqprimerapell')}")
            self.win_login.close()
            self.ventana_principal()
        else:
            QMessageBox.critical(self.win_login, "Error", "Usuario o contraseña incorrectos")

    # --------- registro taquillero ----------
    def abrir_registro_taquillero(self):
        self.win_login.close()
        self.win_registro_taquillero()

    def win_registro_taquillero(self):
        w = QWidget()
        w.setWindowTitle("Registro de Taquillero")
        w.setGeometry(100, 100, 460, 520)
        w.setStyleSheet("background-color: #f2f2f2; font-family: 'Segoe UI';")

        layout = QVBoxLayout()
        titulo = QLabel("Registrar Taquillero")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #1181c3; font-size: 18pt; font-weight: bold; padding: 12px;")
        layout.addWidget(titulo)

        campos = [("Nombre", ""), ("Primer Apellido", ""), ("Segundo Apellido", ""),
                  ("Usuario", ""), ("Contraseña", "")]
        self.entradas = {}
        for etiqueta, _ in campos:
            layout.addWidget(QLabel(etiqueta + ":"))
            e = QLineEdit()
            if etiqueta == "Contraseña":
                e.setEchoMode(QLineEdit.Password)
            layout.addWidget(e)
            self.entradas[etiqueta] = e

        btn_registrar = QPushButton("Registrar")
        btn_registrar.setStyleSheet("background-color: #ed7237; color: white; font-weight: bold; height: 30px;")
        btn_registrar.clicked.connect(lambda: self.registrar(w))
        layout.addWidget(btn_registrar)

        btn_volver = QPushButton("Volver")
        btn_volver.setStyleSheet("background-color: #1181c3; color: white; height: 30px;")
        btn_volver.clicked.connect(lambda: [w.close(), self.ventana_login()])
        layout.addWidget(btn_volver)

        w.setLayout(layout)
        w.show()

    def registrar(self, ventana):
        nombre = self.entradas["Nombre"].text().strip()
        ap1 = self.entradas["Primer Apellido"].text().strip()
        ap2 = self.entradas["Segundo Apellido"].text().strip()
        usuario = self.entradas["Usuario"].text().strip()
        contrasena = self.entradas["Contraseña"].text().strip()
        if not (nombre and ap1 and usuario and contrasena):
            QMessageBox.warning(None, "Atención", "Completa los campos obligatorios")
            return
        ok, err = registrar_taquillero_bd(nombre, ap1, ap2, usuario, contrasena)
        if ok:
            QMessageBox.information(None, "Éxito", "Taquillero registrado correctamente")
            ventana.close()
            self.ventana_login()
        else:
            QMessageBox.critical(None, "Error", f"No se pudo registrar: {err}")

    # --------- ventana principal tras login ----------
    def ventana_principal(self):
        self.main = QWidget()
        self.main.setWindowTitle("Rutas Baja Express - Panel")
        self.main.setGeometry(100, 100, 600, 400)
        self.main.setStyleSheet("background-color: #f2f2f2; font-family: 'Segoe UI';")

        layout = QVBoxLayout()

        titulo = QLabel("Panel principal")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #1181c3; font-size: 18pt; font-weight: bold; padding: 12px;")
        layout.addWidget(titulo)

        bienvenida = QLabel(f"Bienvenido {self.usuario_actual['taqnombre']} {self.usuario_actual['taqprimerapell']}")
        bienvenida.setAlignment(Qt.AlignCenter)
        layout.addWidget(bienvenida)

        btn_logout = QPushButton("Cerrar sesión")
        btn_logout.setStyleSheet("background-color: #d9534f; color: white; height: 40px; font-weight: bold;")
        btn_logout.clicked.connect(self.cerrar_sesion)
        layout.addWidget(btn_logout, alignment=Qt.AlignCenter)

        self.main.setLayout(layout)
        self.main.show()

    def cerrar_sesion(self):
        confirm = QMessageBox.question(self.main, "Confirmar", "¿Cerrar sesión?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.main.close()
            self.usuario_actual = None
            self.ventana_login()

# ---------------------------
# Ejecutar app
# ---------------------------
if __name__ == "__main__":
    App()
