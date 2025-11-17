from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QColorDialog,
    QScrollArea, QFrame, QMessageBox
)
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt
from conexion import crear_conexion

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import os


class VentanaTicketVisual(QWidget):
    def __init__(self, id_pago):
        super().__init__()
        self.id_pago = id_pago
        self.setWindowTitle("Boletos generados")
        self.setMinimumSize(700, 600)
        self.setStyleSheet("background-color: white;")

        self.boletos = []
        self.colores_boletos = []

        layout = QVBoxLayout(self)

        titulo = QLabel("Boletos generados")
        titulo.setFont(QFont("Arial", 20, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)

        self.contenedor = QVBoxLayout()
        contenedor_widget = QWidget()
        contenedor_widget.setLayout(self.contenedor)
        self.scroll.setWidget(contenedor_widget)

        self.cargar_boletos()

        self.btn_imprimir = QPushButton("Imprimir en PDF")
        self.btn_imprimir.clicked.connect(self.imprimir_pdf)
        layout.addWidget(self.btn_imprimir)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.close)
        layout.addWidget(self.btn_ok)

    def cargar_boletos(self):
        db = crear_conexion()
        cursor = db.cursor()

        cursor.execute("""
            SELECT t.codigo, t.precio, t.fechaEmision, t.asiento, t.viaje,
                   p.paNombre, p.paPrimerApell, tp.descripcion, tp.descuento,
                   tpago.nombre
            FROM ticket t
            JOIN pasajero p ON t.pasajero = p.num
            JOIN tipo_pasajero tp ON t.tipopasajero = tp.num
            JOIN pago pg ON t.pago = pg.numero
            JOIN tipo_pago tpago ON pg.tipo = tpago.numero
            WHERE t.pago = %s
        """, (self.id_pago,))
        boletos = cursor.fetchall()
        db.close()

        for boleto in boletos:
            self.boletos.append(boleto)
            self.colores_boletos.append("#f0f0f0")
            self.agregar_boleto(boleto, len(self.boletos) - 1)

    def agregar_boleto(self, datos, index):
        codigo, precio, fecha, asiento, viaje, nombre, apellido, tipo, desc, metodo = datos

        tarjeta = QFrame()
        tarjeta.setFrameShape(QFrame.Box)
        tarjeta.setStyleSheet(f"background-color: {self.colores_boletos[index]}; border-radius: 10px;")
        tarjeta_layout = QVBoxLayout(tarjeta)

        info = f"""
        <b>Pasajero:</b> {nombre} {apellido}<br>
        <b>Asiento:</b> {asiento}<br>
        <b>Tipo:</b> {tipo} ({desc}% desc.)<br>
        <b>Precio:</b> ${precio:.2f}<br>
        <b>Pago:</b> {metodo}<br>
        <b>Fecha:</b> {fecha.strftime('%Y-%m-%d %H:%M')}
        """
        etiqueta = QLabel(info)
        etiqueta.setTextFormat(Qt.RichText)
        etiqueta.setStyleSheet("font-size: 12pt; color: #333;")
        tarjeta_layout.addWidget(etiqueta)

        btn_color = QPushButton("Cambiar color")
        btn_color.clicked.connect(lambda: self.cambiar_color(index, tarjeta))
        tarjeta_layout.addWidget(btn_color)

        self.contenedor.addWidget(tarjeta)

    def cambiar_color(self, index, tarjeta):
        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            tarjeta.setStyleSheet(f"background-color: {hex_color}; border-radius: 10px;")
            self.colores_boletos[index] = hex_color

    def imprimir_pdf(self):
        try:
            filename = f"boletos_pago_{self.id_pago}.pdf"
            c = canvas.Canvas(filename, pagesize=letter)
            width, height = letter

            y = height - 100
            for i, boleto in enumerate(self.boletos):
                codigo, precio, fecha, asiento, viaje, nombre, apellido, tipo, desc, metodo = boleto
                color = self.colores_boletos[i]

                c.setFillColor(HexColor(color))
                c.roundRect(50, y - 90, 500, 80, 10, fill=1)

                c.setFillColor(HexColor("#1181c3"))
                c.setFont("Helvetica-Bold", 12)
                c.drawString(60, y - 30, f"Pasajero: {nombre} {apellido}")
                c.drawString(60, y - 45, f"Asiento: {asiento}   Tipo: {tipo} ({desc}% desc.)")
                c.drawString(60, y - 60, f"Precio: ${precio:.2f}   Pago: {metodo}")
                c.drawString(60, y - 75, f"Fecha: {fecha.strftime('%Y-%m-%d %H:%M')}")

                y -= 110
                if y < 120:
                    c.showPage()
                    y = height - 100

            c.save()
            QMessageBox.information(self, "PDF generado", f"Se creó el archivo: {os.path.abspath(filename)}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el PDF:\n{e}")
