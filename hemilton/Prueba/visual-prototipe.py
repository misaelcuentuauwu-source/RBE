#!/usr/bin/env python3
# visual-prototype.py
# Sistema: login y registro de taquilleros con PySide6
# Autor: adaptado para Misael

import sys
from datetime import date
from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QComboBox, QCheckBox, QDialog
)
from PySide6.QtCore import Qt

from PySide6.QtWidgets import QHeaderView
from conexion import crear_conexion
from panel_principal import PanelPrincipal
from panel_admin import PanelAdministrador
from animacion import Animador
from viajes_programados import ProgramacionWindow

# ===========================
# 🔐 CONFIGURACIÓN DE SEGURIDAD
# ===========================
CLAVE_MAESTRA = "RutasBaja2024"  # Cambia esta clave por una segura en producción

# ===========================
# 🚀 FUNCIONES DE BASE DE DATOS
# ===========================

def iniciar_sesion_bd(usuario, contrasena):
    try:
        cn = crear_conexion()
        cur = cn.cursor(dictionary=True)
        cur.execute("""
            SELECT * FROM taquillero
            WHERE usuario=%s AND contraseña=%s
        """, (usuario, contrasena))
        row = cur.fetchone()
        cur.close()
        cn.close()
        return row
    except Exception as e:
        QMessageBox.critical(None, "Error BD", f"Error al conectar: {e}")
        return None

def registrar_taquillero_bd(nombre, ap1, ap2, usuario, contrasena, terminal=1, supervisa=False):
    try:
        cn = crear_conexion()
        cur = cn.cursor()
        fecha_contrato = date.today()
        cur.execute("""
            INSERT INTO taquillero
            (taqNombre, taqPrimerApell, taqSegundoApell,
             fechaContrato, usuario, contraseña, terminal, supervisa)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, ap1, ap2, fecha_contrato, usuario, contrasena, terminal, supervisa))
        cn.commit()
        cur.close()
        cn.close()
        return True, None
    except Exception as e:
        return False, str(e)

# ===========================
# 🔐 VENTANA DE VERIFICACIÓN DE CLAVE MAESTRA
# ===========================
class VerificacionClave(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Verificación de Seguridad")
        self.setModal(True)
        self.setFixedSize(350, 180)

        layout = QVBoxLayout()

        self.setStyleSheet("""
            QDialog {
                background-color: #f2f2f2;
                font-family: 'Segoe UI';
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1181c3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0d6aa0;
            }
        """)

        label = QLabel("Ingrese la clave maestra para continuar:")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.clave_input = QLineEdit()
        self.clave_input.setEchoMode(QLineEdit.Password)
        self.clave_input.setPlaceholderText("Clave maestra")
        layout.addWidget(self.clave_input)

        self.btn_verificar = QPushButton("Verificar")
        self.btn_verificar.clicked.connect(self.verificar_clave)
        layout.addWidget(self.btn_verificar)

        self.setLayout(layout)

    def verificar_clave(self):
        if self.clave_input.text() == CLAVE_MAESTRA:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Clave incorrecta. Intente nuevamente.")
            self.clave_input.clear()

# ===========================
# 🚀 INTERFAZ GRÁFICA
# ===========================

class App:
    def __init__(self):
        self.usuario_actual = None
        self.animaciones_activas = []
        self.app = QApplication(sys.argv)
        self.ventana_login()
        sys.exit(self.app.exec())

    # ===========================
    # ✨ FUNCIÓN DE TRANSICIÓN
    # ===========================
    def transicion(self, ventana_vieja, ventana_nueva):
        ventana_nueva.setGeometry(ventana_vieja.geometry())
        ventana_nueva.show()
        anim = Animador()
        anim.transicion_fade(ventana_vieja, ventana_nueva)
        anim.anim_group.finished.connect(lambda: ventana_vieja.close())
        anim.anim_group.finished.connect(lambda: self.animaciones_activas.remove(anim))
        self.animaciones_activas.append(anim)

    # ===========================
    # VENTANA LOGIN (Qt Designer)
    # ===========================
    def ventana_login(self):
        from ventanas.login import Ui_loginWindow

        self.win_login = QMainWindow()
        self.win_login.setWindowTitle("Rutas Baja Express - Inicio de Sesión")
        self.win_login.setGeometry(100, 100, 480, 500)

        self.login_ui = Ui_loginWindow()
        self.login_ui.setupUi(self.win_login)

        # Conectar botones a funciones
        self.login_ui.pushButton_5.clicked.connect(self.intentar_login)  # Acceder
        self.login_ui.pushButton_6.clicked.connect(self.verificar_antes_de_registrar)  # Registrarse

        self.win_login.show()

    # ===========================
    # VERIFICACIÓN ANTES DE REGISTRAR
    # ===========================
    def verificar_antes_de_registrar(self):
        dialog = VerificacionClave(self.win_login)
        if dialog.exec() == QDialog.Accepted:
            self.abrir_registro_taquillero()

    # ===========================
    # LOGIN
    # ===========================
    def intentar_login(self):
        usuario = self.login_ui.lineEdit_4.text().strip()
        contrasena = self.login_ui.lineEdit_5.text().strip()

        if not usuario or not contrasena:
            QMessageBox.warning(self.win_login, "Atención", "Completa todos los campos")
            return

        fila = iniciar_sesion_bd(usuario, contrasena)
        if fila:
            self.usuario_actual = fila
            QMessageBox.information(
                self.win_login,
                "Bienvenido",
                f"Hola {fila.get('taqNombre')} {fila.get('taqPrimerApell')}"
            )

            if fila.get("supervisa", 0) == 1:
                nueva = PanelAdministrador(self.usuario_actual, self.ventana_login)
            else:
                nueva = PanelPrincipal(self.usuario_actual, self.ventana_login)

            self.transicion(self.win_login, nueva)
        else:
            QMessageBox.critical(self.win_login, "Error", "Usuario o contraseña incorrectos")

    # ===========================
    # REGISTRO (CON TRANSICIÓN)
    # ===========================
    def abrir_registro_taquillero(self):
        nueva = self.win_registro_taquillero(retornar=True)
        self.transicion(self.win_login, nueva)

    def win_registro_taquillero(self, retornar=False):
        w = QWidget()
        w.setWindowTitle("Registro de Taquillero")
        w.setGeometry(100, 100, 460, 550)
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

        layout.addWidget(QLabel("Terminal:"))
        self.combo_terminal = QComboBox()

        try:
            cn = crear_conexion()
            cur = cn.cursor(dictionary=True)
            cur.execute("SELECT numero, nombre FROM terminal")
            for t in cur.fetchall():
                self.combo_terminal.addItem(t["nombre"], t["numero"])
            cur.close()
            cn.close()
        except Exception as e:
            QMessageBox.critical(None, "Error BD", f"No se pudo cargar las terminales: {e}")
            return
        layout.addWidget(self.combo_terminal)

        self.chk_supervisor = QCheckBox("Supervisor")
        layout.addWidget(self.chk_supervisor)

        btn_registrar = QPushButton("Registrar")
        btn_registrar.setStyleSheet("background-color: #ed7237; color: white; font-weight: bold; height: 30px;")
        btn_registrar.clicked.connect(lambda: self.verificar_antes_de_registrar_bd(w))
        layout.addWidget(btn_registrar)

        btn_volver = QPushButton("Volver")
        btn_volver.setStyleSheet("background-color: #1181c3; color: white; height: 30px;")
        btn_volver.clicked.connect(lambda: self.transicion(w, self.recrear_login()))
        layout.addWidget(btn_volver)

        w.setLayout(layout)
        if retornar:
            return w
        else:
            w.show()

    # ===========================
    # VERIFICACIÓN ANTES DE REGISTRAR EN BD
    # ===========================
    def verificar_antes_de_registrar_bd(self, ventana):
        dialog = VerificacionClave(ventana)
        if dialog.exec() == QDialog.Accepted:
            self.registrar(ventana)

    # ===========================
    # VOLVER A LOGIN (CON ANIMACIÓN)
    # ===========================
    def recrear_login(self):
        self.ventana_login()
        return self.win_login

    # ===========================
    # REGISTRAR BD
    # ===========================
    def registrar(self, ventana):
        nombre = self.entradas["Nombre"].text().strip()
        ap1 = self.entradas["Primer Apellido"].text().strip()
        ap2 = self.entradas["Segundo Apellido"].text().strip()
        usuario = self.entradas["Usuario"].text().strip()
        contrasena = self.entradas["Contraseña"].text().strip()

        if not (nombre and ap1 and usuario and contrasena):
            QMessageBox.warning(None, "Atención", "Completa los campos obligatorios")
            return

        terminal = self.combo_terminal.currentData()
        supervisa = self.chk_supervisor.isChecked()

        ok, err = registrar_taquillero_bd(nombre, ap1, ap2, usuario, contrasena, terminal, supervisa)
        if ok:
            QMessageBox.information(None, "Éxito", "Taquillero registrado correctamente")
            self.transicion(ventana, self.recrear_login())
        else:
            QMessageBox.critical(None, "Error", f"No se pudo registrar: {err}")

# ===========================
# 🚀 Ejecutar app
# ===========================
if __name__ == "__main__":
    App()
