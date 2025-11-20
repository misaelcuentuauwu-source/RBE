from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton,
    QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from conexion import crear_conexion
from pasajero import VentanaRegistroPasajero
from precio import VentanaPrecio   # nueva ventana para calcular precio


class SeleccionarAsiento(QWidget):
    def __init__(self, id_viaje, taquillero_id=200):
        super().__init__()
        self.id_viaje = id_viaje
        self.taquillero_id = taquillero_id
        self.setWindowTitle(f"Asientos disponibles – Viaje {id_viaje}")
        self.setMinimumSize(700, 550)
        self.setStyleSheet(self.estilos())

        self.asientos_seleccionados = []
        self.botones_asientos = []
        self.asiento_index = 0
        self.boletos_pendientes = []  # lista de (pasajero_id, asiento_id)

        layout = QVBoxLayout(self)

        titulo = QLabel(f"Asientos del viaje {id_viaje}")
        titulo.setFont(QFont("Arial", 20, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        self.grid = QGridLayout()
        layout.addLayout(self.grid)

        self.cargar_asientos()

        self.btn_confirmar = QPushButton("Confirmar asientos ✔")
        self.btn_confirmar.setObjectName("botonPrincipal")
        self.btn_confirmar.clicked.connect(self.confirmar_asientos)
        layout.addWidget(self.btn_confirmar, alignment=Qt.AlignRight)

    def cargar_asientos(self):
        db = crear_conexion()
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(*) FROM viaje_asiento WHERE viaje = %s", (self.id_viaje,))
        total = cursor.fetchone()[0]

        if total == 0:
            cursor.execute("""
                INSERT INTO viaje_asiento (asiento, viaje, ocupado)
                SELECT a.numero, %s, 0
                FROM asiento a
                WHERE a.autobus = (
                    SELECT autobus FROM viaje WHERE numero = %s
                )
            """, (self.id_viaje, self.id_viaje))
            db.commit()

        cursor.execute("""
            SELECT a.numero, va.ocupado
            FROM viaje_asiento va
            JOIN asiento a ON va.asiento = a.numero
            WHERE va.viaje = %s
            ORDER BY a.numero
        """, (self.id_viaje,))
        asientos = cursor.fetchall()
        db.close()

        columnas = 4
        for i, (num_asiento, ocupado) in enumerate(asientos):
            fila = i // columnas
            col = i % columnas
            letra = chr(65 + col)
            etiqueta = f"{fila + 1}{letra}"

            btn = QPushButton(etiqueta)
            btn.setFixedSize(60, 40)
            btn.setProperty("id_asiento", num_asiento)

            if ocupado:
                btn.setStyleSheet("background-color: #ccc; color: #666;")
                btn.setEnabled(False)
            else:
                btn.setStyleSheet("background-color: #4CAF50; color: white;")
                btn.clicked.connect(self.seleccionar_asiento)

            self.grid.addWidget(btn, fila, col)
            self.botones_asientos.append(btn)

    def seleccionar_asiento(self):
        btn = self.sender()
        id_asiento = btn.property("id_asiento")

        if id_asiento in self.asientos_seleccionados:
            self.asientos_seleccionados.remove(id_asiento)
            btn.setStyleSheet("background-color: #4CAF50; color: white;")
        else:
            self.asientos_seleccionados.append(id_asiento)
            btn.setStyleSheet("background-color: #0078ff; color: white;")

    def confirmar_asientos(self):
        if not self.asientos_seleccionados:
            QMessageBox.warning(self, "Aviso", "Selecciona al menos un asiento.")
            return

        self.asiento_index = 0
        self.boletos_pendientes = []
        self.abrir_registro_para_asiento()

    def abrir_registro_para_asiento(self):
        asiento_id = self.asientos_seleccionados[self.asiento_index]
        numero_pasajero = self.asiento_index + 1

        self.ventana_registro = VentanaRegistroPasajero(numero_pasajero, asiento_id)
        self.ventana_registro.pasajero_registrado.connect(self.procesar_pasajero)
        self.ventana_registro.show()

    def procesar_pasajero(self, pasajero_id):
        asiento_id = self.asientos_seleccionados[self.asiento_index]
        self.boletos_pendientes.append((pasajero_id, asiento_id))

        self.asiento_index += 1
        if self.asiento_index < len(self.asientos_seleccionados):
            self.abrir_registro_para_asiento()
        else:
            # Al terminar todos los registros → abrir ventana de precio
            self.ventana_precio = VentanaPrecio(self.id_viaje, self.taquillero_id, self.boletos_pendientes)
            self.ventana_precio.show()
            self.close()

    def estilos(self):
        return """
        #titulo {
            color: #333;
        }
        #botonPrincipal {
            background-color: #0078ff;
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            font-size: 15px;
        }
        #botonPrincipal:hover {
            background-color: #005fcc;
        }
        """
