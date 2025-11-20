import mysql.connector
from datetime import date
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QDateEdit
)
from PySide6.QtCore import Qt


class VentanaRegistroPasajero(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrar Pasajero")
        self.setGeometry(300, 200, 450, 500)

        self.setStyleSheet("""
            QWidget { background-color: #f7f9fb; font-family: 'Segoe UI'; }
            QLabel { font-size: 12pt; color: #333; }
            QLineEdit, QDateEdit {
                padding: 6px; border-radius: 6px;
                border: 1px solid #b6b6b6; background-color: white;
            }
            QPushButton {
                background-color: #1181c3; color: white;
                padding: 10px; font-size: 12pt; border-radius: 6px;
            }
            QPushButton:hover { background-color: #0d6ca4; }
        """)

        layout = QVBoxLayout(self)

        # -----------------------------
        # TÍTULO
        # -----------------------------
        titulo = QLabel("Registro de Pasajero")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 20pt; font-weight: bold; color: #1181c3;")
        layout.addWidget(titulo)

        # -----------------------------
        # CAMPOS
        # -----------------------------
        layout.addWidget(QLabel("Nombre"))
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre de pila")
        layout.addWidget(self.input_nombre)

        layout.addWidget(QLabel("Apellido paterno"))
        self.input_apellidop = QLineEdit()
        self.input_apellidop.setPlaceholderText("Primer apellido")
        layout.addWidget(self.input_apellidop)

        layout.addWidget(QLabel("Apellido materno"))
        self.input_apellidom = QLineEdit()
        self.input_apellidom.setPlaceholderText("Segundo apellido")
        layout.addWidget(self.input_apellidom)

        layout.addWidget(QLabel("Fecha de nacimiento"))
        self.input_nacimiento = QDateEdit()
        self.input_nacimiento.setDisplayFormat("yyyy-MM-dd")
        self.input_nacimiento.setCalendarPopup(True)
        self.input_nacimiento.setDate(date(2000, 1, 1))
        layout.addWidget(self.input_nacimiento)

        # -----------------------------
        # BOTÓN
        # -----------------------------
        self.btn_registrar = QPushButton("Registrar pasajero")
        self.btn_registrar.clicked.connect(self.registrar_pasajero)
        layout.addWidget(self.btn_registrar)

    # ---------------------------------------
    # CALCULAR EDAD
    # ---------------------------------------
    def calcular_edad(self, nacimiento):
        hoy = date.today()
        edad = hoy.year - nacimiento.year
        if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
            edad -= 1
        return edad

    # ---------------------------------------
    # REGISTRO EN LA BASE DE DATOS
    # ---------------------------------------
    def registrar_pasajero(self):
        nombre = self.input_nombre.text().strip()
        apep = self.input_apellidop.text().strip()
        apem = self.input_apellidom.text().strip()
        nacimiento = self.input_nacimiento.date().toPython()

        # Validaciones
        if not nombre or not apep or not apem:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        edad = self.calcular_edad(nacimiento)

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="prototipo"
            )
            cursor = conexion.cursor()

            query = """
                INSERT INTO pasajeros (panombre, paprimerapell, pasegundoapell, fechanacimiento, edad)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (nombre, apep, apem, nacimiento, edad))
            conexion.commit()

            QMessageBox.information(self, "Éxito", "Pasajero registrado correctamente.")
            conexion.close()

            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el pasajero:\n{e}")
