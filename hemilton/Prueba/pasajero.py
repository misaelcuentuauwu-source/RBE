from datetime import date
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QDateEdit
)
from PySide6.QtCore import Qt, Signal
from conexion import crear_conexion


class VentanaRegistroPasajero(QWidget):
    pasajero_registrado = Signal(int)

    def __init__(self, numero_pasajero=1, asiento_id=None):
        super().__init__()
        self.numero_pasajero = numero_pasajero
        self.asiento_id = asiento_id

        self.setWindowTitle(f"Registrar Pasajero {numero_pasajero}")
        self.setGeometry(300, 200, 450, 500)

        layout = QVBoxLayout(self)

        titulo = QLabel(f"Registro de Pasajero {numero_pasajero}")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18pt; font-weight: bold; color: #1181c3;")
        layout.addWidget(titulo)

        if self.asiento_id is not None:
            info = QLabel(f"Asiento seleccionado: {self.asiento_id}")
            info.setAlignment(Qt.AlignCenter)
            layout.addWidget(info)

        layout.addWidget(QLabel("Nombre"))
        self.input_nombre = QLineEdit()
        layout.addWidget(self.input_nombre)

        layout.addWidget(QLabel("Apellido paterno"))
        self.input_apellidop = QLineEdit()
        layout.addWidget(self.input_apellidop)

        layout.addWidget(QLabel("Apellido materno (opcional)"))
        self.input_apellidom = QLineEdit()
        layout.addWidget(self.input_apellidom)

        layout.addWidget(QLabel("Fecha de nacimiento"))
        self.input_nacimiento = QDateEdit()
        self.input_nacimiento.setDisplayFormat("yyyy-MM-dd")
        self.input_nacimiento.setCalendarPopup(True)
        self.input_nacimiento.setDate(date(2000, 1, 1))
        layout.addWidget(self.input_nacimiento)

        self.btn_registrar = QPushButton("Registrar pasajero")
        self.btn_registrar.clicked.connect(self.registrar_pasajero)
        layout.addWidget(self.btn_registrar)

    def calcular_edad(self, nacimiento):
        hoy = date.today()
        edad = hoy.year - nacimiento.year
        if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
            edad -= 1
        return edad

    def registrar_pasajero(self):
        nombre = self.input_nombre.text().strip()
        apep = self.input_apellidop.text().strip()
        apem = self.input_apellidom.text().strip()
        nacimiento = self.input_nacimiento.date().toPython()

        # Validaciones
        if not nombre or not apep:
            QMessageBox.warning(self, "Error", "Nombre y apellido paterno son obligatorios.")
            return

        edad = self.calcular_edad(nacimiento)

        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()

            query = """
                INSERT INTO pasajero (paNombre, paPrimerApell, paSegundoApell, fechaNacimiento, edad)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (nombre, apep, apem if apem else None, nacimiento, edad))
            conexion.commit()

            pasajero_id = cursor.lastrowid

            QMessageBox.information(self, "Éxito", f"Pasajero {self.numero_pasajero} registrado correctamente.")
            conexion.close()

            ## Mandar señal ##
            self.pasajero_registrado.emit(pasajero_id)
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el pasajero:\n{e}")
