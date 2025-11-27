# ventana_pago_responsive.py

from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QComboBox, QLineEdit, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
import recursos_rc


# ============================================
# FUNCIÓN PARA CREAR IMÁGENES RESPONSIVE
# ============================================
def crear_imagen_r(path, max_w, max_h):
    lbl = QLabel()
    lbl.setAlignment(Qt.AlignCenter)
    lbl.original_pixmap = QPixmap(path)
    lbl.max_w = max_w
    lbl.max_h = max_h
    lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return lbl


class VentanaPago(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pago")
        self.resize(1100, 760)

        # ======================================
        # LAYOUT PRINCIPAL
        # ======================================
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # ======================================
        # PANEL IZQUIERDO
        # ======================================
        panel_izq = QWidget()
        panel_izq.setStyleSheet("background: white;")
        layout_principal.addWidget(panel_izq, 3)

        layout_izq = QVBoxLayout(panel_izq)
        layout_izq.setAlignment(Qt.AlignCenter)

        # =============== IMÁGENES RESPONSIVE (IZQUIERDA) ===============
        self.img = crear_imagen_r(":/recursos/Cartoon-style illust.png", 450, 450)
        self.logo = crear_imagen_r(":/recursos/Convierte el logo de.png", 350, 350)

        layout_izq.addWidget(self.img)
        layout_izq.addWidget(self.logo)
        layout_izq.addStretch()

        # ======================================
        # PANEL DERECHO con SCROLL RESPONSIVE
        # ======================================
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: #0074B7; border: none;")
        layout_principal.addWidget(scroll, 4)

        contenedor_der = QWidget()
        scroll.setWidget(contenedor_der)

        layout_der = QVBoxLayout(contenedor_der)
        layout_der.setAlignment(Qt.AlignTop)

        # ======================================
        # TARJETA
        # ======================================
        tarjeta = QFrame()
        tarjeta.setStyleSheet("""
            background: #2A9BE7;
            border-radius: 25px;
        """)
        tarjeta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout_tarjeta = QVBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(40, 20, 40, 30)
        layout_tarjeta.setSpacing(18)

        layout_der.addWidget(tarjeta, alignment=Qt.AlignCenter)

        # ======================================
        # ICONO Y TEXTOS
        # ======================================

        # Imagen derecha RESPONSIVE (arreglo)
        self.icono = crear_imagen_r(":/recursos/logocirculo.png", 120, 120)

        titulo = QLabel("Pago")
        titulo.setFont(QFont("Arial", 32, QFont.Bold))
        titulo.setStyleSheet("color: white;")

        subtitulo = QLabel("Resumen de compra")
        subtitulo.setStyleSheet("color: #E9E9E9; font-size: 16px;")

        layout_tarjeta.addWidget(self.icono, alignment=Qt.AlignCenter)
        layout_tarjeta.addWidget(titulo, alignment=Qt.AlignCenter)
        layout_tarjeta.addWidget(subtitulo, alignment=Qt.AlignCenter)

        # ======================================
        # TARJETAS DE INFORMACIÓN
        # ======================================
        def crear_info(nombre, valor):
            cont = QFrame()
            cont.setStyleSheet("""
                background: white;
                border-radius: 15px;
            """)
            cont.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            lay = QVBoxLayout(cont)
            lay.setContentsMargins(14, 10, 14, 10)

            lbl1 = QLabel(nombre)
            lbl1.setStyleSheet("color: #555; font-size: 14px;")

            lbl2 = QLabel(valor)
            lbl2.setFont(QFont("Arial", 18, QFont.Bold))

            lay.addWidget(lbl1)
            lay.addWidget(lbl2)

            return cont, lbl2

        self.info_boletos, self.lbl_boletos = crear_info("Cantidad de boletos", "0")
        self.info_total, self.lbl_total = crear_info("Total de compra", "$0")

        fila = QHBoxLayout()
        fila.addWidget(self.info_boletos)
        fila.addWidget(self.info_total)
        layout_tarjeta.addLayout(fila)

        # ======================================
        # 🔵 BOTÓN "VER DETALLE"
        # ======================================
        self.btn_detalle = QPushButton("Ver detalle")
        self.btn_detalle.setStyleSheet("""
            QPushButton {
                background: white;
                padding: 10px;
                border-radius: 15px;
                font-size: 16px;
            }
        """)
        layout_tarjeta.addWidget(self.btn_detalle)

        # ======================================
        # MÉTODO DE PAGO
        # ======================================

        # ✔️ Aquí se crea el ComboBox ANTES de estilizarlo (corrección)
        self.metodo_pago = QComboBox()
        self.metodo_pago.addItems(["Efectivo", "Tarjeta"])

        # ✔️ Estilo moderno (fondo blanco al abrir)
        self.metodo_pago.setStyleSheet("""
            QComboBox {
                background: white;
                padding: 10px;
                border-radius: 12px;
                font-size: 16px;
                border: 2px solid #cccccc;
            }
            QComboBox:hover {
                border: 2px solid #2A9BE7;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                background: white;
                color: black;
                selection-background-color: #2A9BE7;
                selection-color: white;
                border-radius: 8px;
                padding: 6px;
            }
        """)

        layout_tarjeta.addWidget(self.metodo_pago)

        # ======================================
        # ÁREA DINÁMICA
        # ======================================
        self.area_dinamica = QVBoxLayout()
        layout_tarjeta.addLayout(self.area_dinamica)

        self.metodo_pago.currentTextChanged.connect(self.actualizar_area_pago)
        self.actualizar_area_pago("Efectivo")

        # ======================================
        # BOTONES
        # ======================================
        botones = QHBoxLayout()

        btn_confirmar = QPushButton("Confirmar")
        btn_confirmar.setStyleSheet("""
            background: #004C90;
            color: white;
            border-radius: 15px;
            padding: 12px;
        """)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("""
            background: #FF7A00;
            color: white;
            border-radius: 15px;
            padding: 12px;
        """)

        botones.addWidget(btn_confirmar)
        botones.addWidget(btn_cancelar)
        layout_tarjeta.addLayout(botones)

    # ======================================
    # ÁREA DINÁMICA
    # ======================================
    def actualizar_area_pago(self, metodo):
        while self.area_dinamica.count():
            item = self.area_dinamica.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if metodo == "Efectivo":
            total = QLabel("Total: $0")
            total.setStyleSheet("color: white; font-size: 18px;")

            recibido = QLineEdit()
            recibido.setPlaceholderText("Total recibido")
            recibido.setStyleSheet("""
                background: white;
                padding: 10px;
                border-radius: 15px;
            """)

            cambio = QLabel("Cambio: $0")
            cambio.setStyleSheet("color: white; font-size: 18px;")

            self.area_dinamica.addWidget(total)
            self.area_dinamica.addWidget(recibido)
            self.area_dinamica.addWidget(cambio)

        else:
            for txt in ["Número de tarjeta", "Mes (MM)", "Año (YY)", "CVV"]:
                entrada = QLineEdit()
                entrada.setPlaceholderText(txt)
                entrada.setStyleSheet("""
                    background: white;
                    padding: 10px;
                    border-radius: 15px;
                """)
                self.area_dinamica.addWidget(entrada)

    # ======================================
    # REDIMENSIONADO DE IMÁGENES RESPONSIVO
    # ======================================
    def resizeEvent(self, event):
        for lbl in [self.img, self.logo, self.icono]:
            pix = lbl.original_pixmap
            if not pix.isNull():
                lbl.setPixmap(
                    pix.scaled(
                        min(lbl.width(), lbl.max_w),
                        min(lbl.height(), lbl.max_h),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )
        return super().resizeEvent(event)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    v = VentanaPago()
    v.show()
    sys.exit(app.exec())