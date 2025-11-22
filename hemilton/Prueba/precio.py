from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit,
    QPushButton, QMessageBox
)
from PySide6.QtWidgets import QMessageBox

from PySide6.QtCore import Signal
from conexion import crear_conexion
from ventana_ticket import VentanaTicketVisual  # Importar la ventana visual de boletos


class VentanaPrecio(QWidget):
    precio_confirmado = Signal(list)

    def __init__(self, id_viaje, taquillero_id, boletos_pendientes):
        super().__init__()
        self.id_viaje = id_viaje
        self.taquillero_id = taquillero_id
        self.boletos_pendientes = boletos_pendientes

        self.setWindowTitle("Confirmar Pago")
        self.setGeometry(350, 250, 500, 500)

        layout = QVBoxLayout(self)

        titulo = QLabel("Confirmar Pago y Generar Tickets")
        titulo.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1181c3;")
        layout.addWidget(titulo)

        # Tipo de pasajero
        layout.addWidget(QLabel("Tipo de pasajero"))
        self.combo_tipo = QComboBox()
        self.cargar_tipos_pasajero()
        self.combo_tipo.currentIndexChanged.connect(self.calcular_precio)
        layout.addWidget(self.combo_tipo)

        # Precio base
        layout.addWidget(QLabel("Precio base del viaje"))
        self.label_precio_base = QLabel("0.00 MXN")
        layout.addWidget(self.label_precio_base)

        # Precio final
        layout.addWidget(QLabel("Precio final con descuento"))
        self.label_final = QLabel("0.00 MXN")
        layout.addWidget(self.label_final)

        # Método de pago
        layout.addWidget(QLabel("Método de pago"))
        self.combo_pago = QComboBox()
        self.cargar_metodos_pago()
        self.combo_pago.currentIndexChanged.connect(self.toggle_tarjeta_fields)
        layout.addWidget(self.combo_pago)

        # Campos de tarjeta
        self.label_tarjeta = QLabel("Número de tarjeta (últimos 4 dígitos)")
        self.input_tarjeta = QLineEdit()
        self.input_tarjeta.setPlaceholderText("Ejemplo: 1234")

        self.label_banco = QLabel("Banco emisor")
        self.input_banco = QLineEdit()
        self.input_banco.setPlaceholderText("Ejemplo: BBVA")

        layout.addWidget(self.label_tarjeta)
        layout.addWidget(self.input_tarjeta)
        layout.addWidget(self.label_banco)
        layout.addWidget(self.input_banco)

        # Botón confirmar
        self.btn_confirmar = QPushButton("Confirmar y registrar pago")
        self.btn_confirmar.clicked.connect(self.confirmar_pago)
        layout.addWidget(self.btn_confirmar)

        # Inicializar precio base
        self.precio_base = self.obtener_precio_base()
        self.label_precio_base.setText(f"{self.precio_base:.2f} MXN")
        self.calcular_precio()
        self.toggle_tarjeta_fields()

    def cargar_tipos_pasajero(self):
        db = crear_conexion()
        cursor = db.cursor()
        cursor.execute("SELECT num, descripcion, descuento FROM tipo_pasajero")
        self.tipos = cursor.fetchall()
        db.close()

        for num, desc, descu in self.tipos:
            self.combo_tipo.addItem(f"{desc} ({descu}% desc.)", (num, descu))

    def cargar_metodos_pago(self):
        db = crear_conexion()
        cursor = db.cursor()
        cursor.execute("SELECT numero, nombre FROM tipo_pago")
        self.metodos = cursor.fetchall()
        db.close()

        for num, nombre in self.metodos:
            self.combo_pago.addItem(nombre, num)

    def obtener_precio_base(self):
        db = crear_conexion()
        cursor = db.cursor()
        cursor.execute("""
            SELECT r.precio
            FROM viaje v
            JOIN ruta r ON v.ruta = r.codigo
            WHERE v.numero = %s
        """, (self.id_viaje,))
        resultado = cursor.fetchone()
        db.close()
        return float(resultado[0]) if resultado else 0.0

    def calcular_precio(self):
        if self.combo_tipo.currentData() is None:
            return
        tipo_id, descuento = self.combo_tipo.currentData()
        precio_final = self.precio_base - (self.precio_base * descuento / 100)
        self.label_final.setText(f"{precio_final:.2f} MXN")
        self.precio_final = precio_final
        self.tipo_id = tipo_id

    def toggle_tarjeta_fields(self):
        metodo_pago = self.combo_pago.currentData()
        visible = (metodo_pago == 2)
        self.label_tarjeta.setVisible(visible)
        self.input_tarjeta.setVisible(visible)
        self.label_banco.setVisible(visible)
        self.input_banco.setVisible(visible)

    def confirmar_pago(self):
        metodo_pago = self.combo_pago.currentData()

        try:
            db = crear_conexion()
            cursor = db.cursor()

            # Registrar pago
            cursor.execute("""
                INSERT INTO pago (fechapago, monto, tipo, vendedor)
                VALUES (NOW(), %s, %s, %s)
            """, (self.precio_final, metodo_pago, self.taquillero_id))
            id_pago = cursor.lastrowid

            # Validar tarjeta si aplica
            if metodo_pago == 2:
                ultimos4 = self.input_tarjeta.text().strip()
                banco = self.input_banco.text().strip()
                if not ultimos4 or not banco:
                    QMessageBox.warning(self, "Error", "Ingresa los datos de la tarjeta.")
                    return

            # Generar tickets
            for pasajero_id, asiento_id in self.boletos_pendientes:
                cursor.execute("""
                    INSERT INTO ticket (precio, fechaEmision, asiento, viaje, pasajero, tipopasajero, pago)
                    VALUES (%s, NOW(), %s, %s, %s, %s, %s)
                """, (self.precio_final, asiento_id, self.id_viaje, pasajero_id, self.tipo_id, id_pago))

                cursor.execute("""
                    UPDATE viaje_asiento
                    SET ocupado = 1
                    WHERE asiento = %s AND viaje = %s
                """, (asiento_id, self.id_viaje))

            db.commit()
            db.close()

            QMessageBox.information(self, "Éxito", "Pago registrado y tickets generados correctamente.")

            # Abrir ventana de boletos
            self.ventana_ticket = VentanaTicketVisual(id_pago)
            self.ventana_ticket.show()

            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el pago:\n{e}")
