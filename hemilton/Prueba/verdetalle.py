from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QSizePolicy, QScrollArea, QApplication
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import sys


class VentanaDetalle(QWidget):
    def __init__(self, datos_lista=None):
        super().__init__()

        self.setWindowTitle("Detalle del boleto")
        self.resize(1100, 700)
        self.setStyleSheet("background: #0074B7;")

        self.datos_lista = datos_lista or [{}]

        # SCROLL #
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        contenedor = QWidget()
        scroll.setWidget(contenedor)

        layout = QVBoxLayout(contenedor)
        layout.setAlignment(Qt.AlignTop)

        # titulo #
        titulo = QLabel("Detalle de Boletos")
        titulo.setFont(QFont("Arial", 32, QFont.Bold))
        titulo.setStyleSheet("color: white; margin-top: 20px;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Tarjeta #
        def crear_tarjeta(boleto):
            tarjeta = QFrame()
            tarjeta.setStyleSheet("""
                background: #2A9BE7;
                border-radius: 20px;
            """)
            tarjeta.setMinimumHeight(155)
            tarjeta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            tarjeta_layout = QVBoxLayout(tarjeta)
            tarjeta_layout.setContentsMargins(20, 15, 20, 15)
            tarjeta_layout.setSpacing(10)

            # Acomodo para fila superior #
            fila_superior = QFrame()
            fila1 = QHBoxLayout(fila_superior)
            fila1.setSpacing(15)

            def crear_bloque(titulo, valor):
                cont = QFrame()
                cont.setStyleSheet("background: white; border-radius: 10px;")
                cont.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                ly = QVBoxLayout(cont)
                ly.setContentsMargins(10, 6, 10, 6)

                lbl_t = QLabel(titulo)
                lbl_t.setStyleSheet("font-size: 13px; color: #555;")

                lbl_v = QLabel(valor)
                lbl_v.setStyleSheet("font-size: 17px; font-weight: bold; color: #222;")
                lbl_v.setWordWrap(True)

                ly.addWidget(lbl_t)
                ly.addWidget(lbl_v)

                return cont

            fila1.addWidget(crear_bloque("N° Viaje", boleto["num_viaje"]))
            fila1.addWidget(crear_bloque("Pasajero", boleto["nombre_pasajero"]))
            fila1.addWidget(crear_bloque("Asiento", boleto["num_asiento"]))
            fila1.addWidget(crear_bloque("Tipo Asiento", boleto["tipo_asiento"]))
            fila1.addWidget(crear_bloque("Precio", f"${boleto['precio_boleto']}"))

            tarjeta_layout.addWidget(fila_superior)

            # Rutas y Horarios #
            fila_inferior = QFrame()
            fila2 = QVBoxLayout(fila_inferior)
            fila_inferior.setStyleSheet("background: white; border-radius: 12px;")
            fila2.setContentsMargins(15, 10, 15, 10)

            lbl_ruta = QLabel(f"{boleto['origen']} → {boleto['destino']}")
            lbl_ruta.setStyleSheet("font-size: 18px; font-weight: bold; color: #0A4A7A;")
            lbl_ruta.setWordWrap(True)
            fila2.addWidget(lbl_ruta)

            lbl_horas = QLabel(
                f"Salida:  {boleto['salida']}\nLlegada: {boleto['llegada']}"
            )
            lbl_horas.setStyleSheet("font-size: 15px; color: #333;")
            lbl_horas.setWordWrap(True)
            fila2.addWidget(lbl_horas)

            tarjeta_layout.addWidget(fila_inferior)

            return tarjeta

        # Agregar tarjetas #
        total_general = 0
        for boleto in self.datos_lista:
            try:
                total_general += float(boleto["precio_boleto"])
            except:
                pass

            layout.addWidget(crear_tarjeta(boleto))

        # Seccion de abajo #
        seccion_inferior = QFrame()
        seccion_inferior.setStyleSheet("background: white; border-radius: 20px;")
        seccion_layout = QHBoxLayout(seccion_inferior)
        seccion_layout.setContentsMargins(25, 20, 25, 20)

        # IZQUIERDA #
        izquierda = QVBoxLayout()
        lbl_cantidad = QLabel(f"Cantidad de boletos: {len(self.datos_lista)}")
        lbl_descuentos = QLabel("Descuentos aplicados: 0%")

        for l in (lbl_cantidad, lbl_descuentos):
            l.setStyleSheet("font-size: 18px; color: #222;")
            l.setWordWrap(True)

        izquierda.addWidget(lbl_cantidad)
        izquierda.addWidget(lbl_descuentos)

        seccion_layout.addLayout(izquierda)

        # DERECHA #
        derecha = QVBoxLayout()
        lbl_titulo_total = QLabel("TOTAL A PAGAR")
        lbl_titulo_total.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")

        lbl_total = QLabel(f"${total_general:.2f}")
        lbl_total.setStyleSheet("font-size: 30px; font-weight: bold; color: #0A4A7A;")

        derecha.addWidget(lbl_titulo_total, alignment=Qt.AlignRight)
        derecha.addWidget(lbl_total, alignment=Qt.AlignRight)

        seccion_layout.addLayout(derecha)

        layout.addWidget(seccion_inferior)

        # BOTON CERRAR #
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setStyleSheet("""
            background: #004C90;
            color: white;
            border-radius: 15px;
            padding: 10px;
            font-size: 16px;
            margin-bottom: 15px;
        """)
        btn_cerrar.clicked.connect(self.close)

        layout.addWidget(btn_cerrar, alignment=Qt.AlignCenter)

        # Agregar scroll #
        base = QVBoxLayout(self)
        base.addWidget(scroll)


# Main completo #
if __name__ == "__main__":
    app = QApplication(sys.argv)

    datos_demo = [
        {
            "num_viaje": "MX204",
            "salida": "2025-03-15 14:30",
            "llegada": "2025-03-15 18:45",
            "origen": "Guadalajara",
            "destino": "Monterrey",
            "nombre_pasajero": "Luis Hernández",
            "tipo_asiento": "Ejecutivo",
            "num_asiento": "18A",
            "precio_boleto": "850"
        },
        {
            "num_viaje": "MX205",
            "salida": "2025-03-16 08:00",
            "llegada": "2025-03-16 12:20",
            "origen": "Guadalajara",
            "destino": "CDMX",
            "nombre_pasajero": "Ana López",
            "tipo_asiento": "Económico",
            "num_asiento": "10C",
            "precio_boleto": "600"
        }
    ]

    ventana = VentanaDetalle(datos_demo)
    ventana.show()

    sys.exit(app.exec())
    