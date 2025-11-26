# ventana_tipo_pasajero.py
# Nueva ventana con el mismo diseño que la imagen

from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QSizePolicy, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
import recursos_rc


class VentanaTipoPasajero(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tipo de pasajero")
        self.resize(1100, 760)

        self.setStyleSheet("""
    QComboBox {
        background: white;
        border: 2px solid #cccccc;
        border-radius: 10px;
        padding: 6px 10px;
        font-size: 16px;
        min-width: 180px;
    }

    QComboBox:hover {
        border: 2px solid #aaaaaa;
    }

    QComboBox::drop-down {
        border: none;
        width: 30px;
    }

    QComboBox::down-arrow {
        width: 14px;
        height: 14px;
        image: url(:/recursos/down_arrow.svg);
    }

    /* COLOR DEL MENU DESPLEGADO */
    QComboBox QAbstractItemView {
        background: white;
        color: black;
        selection-background-color: #e6e6e6;
        selection-color: black;
        border: 1px solid #cccccc;
    }

    QLabel {
        color: white;
    }
""")  

        # ============================
        # CONTENEDOR PRINCIPAL (2 columnas)
        # ============================
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # ============================
        # PANEL IZQUIERDO (Imagen + texto)
        # ============================
        panel_izquierdo = QWidget()
        panel_izquierdo.setStyleSheet("background: white;")
        layout_izq = QVBoxLayout(panel_izquierdo)
        layout_izq.setAlignment(Qt.AlignCenter)

        # ========= SUPERPOSICIÓN DE IMÁGENES ==========
        contenedor = QWidget()
        contenedor.setFixedSize(500, 520)  # más grande para que no se corten

        # Imagen del camión (arriba)
        img = QLabel(contenedor)
        img.setAttribute(Qt.WA_TranslucentBackground)
        img_pix = QPixmap(":/recursos/Cartoon-style illust.png").scaled(
            500, 420, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        img.setPixmap(img_pix)

        # Centrado horizontal
        img_x = (contenedor.width() - img_pix.width()) // 2
        img.move(img_x, -10)   # un poco arriba

        # Logo Baja California (abajo)
        logo_bc = QLabel(contenedor)
        logo_bc.setAttribute(Qt.WA_TranslucentBackground)
        logo_pix = QPixmap(":/recursos/Convierte el logo de.png").scaled(
            480, 420, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo_bc.setPixmap(logo_pix)

        # Centrado horizontal
        logo_x = (contenedor.width() - logo_pix.width()) // 2
        logo_bc.move(logo_x, 250)  # debajo del camión

        # Orden de capas: camión arriba
        logo_bc.lower()
        img.raise_()

        layout_izq.addWidget(contenedor, alignment=Qt.AlignCenter)

        # ============================
        # PANEL DERECHO (Fondo Azul)
        # ============================
        panel_derecho = QWidget()
        panel_derecho.setStyleSheet("background: #0074B7;")

        layout_der = QVBoxLayout(panel_derecho)
        layout_der.setAlignment(Qt.AlignCenter)

        # ============================
        # TARJETA INTERNA
        # ============================
        tarjeta = QFrame()
        tarjeta.setStyleSheet("""
            background: #2A9BE7;
            border-radius: 20px;
        """)
        tarjeta.setFixedWidth(420)

        layout_tarjeta = QVBoxLayout(tarjeta)
        layout_tarjeta.setAlignment(Qt.AlignTop)
        layout_tarjeta.setContentsMargins(40, 20, 40, 30)  # Más margen para que respire
        layout_tarjeta.setSpacing(18)  # Más separación entre elementos

        # Icono
        icono = QLabel()
        icono.setPixmap(QPixmap(":/recursos/logocirculo.png").scaled(
            110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        icono.setAlignment(Qt.AlignCenter)

        # Título
        titulo = QLabel("Tipo de pasajero")
        titulo.setFont(QFont("Arial", 30, QFont.Bold))
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignCenter)

        # ============================
        # SUBTEXTOS
        # ============================
        texto_desc = QVBoxLayout()
        texto_desc.setSpacing(12)  # un poco más de espacio entre subtítulos

        t1 = QLabel("Lista de descuentos:")
        t2 = QLabel("Niños (Menores a 10 años)")
        t3 = QLabel("Adultos Mayores (A partir de los 60 años)")

        for t in (t1, t2, t3):
            t.setFont(QFont("Arial", 14))
            t.setStyleSheet("color: white;")
            t.setWordWrap(True)
            texto_desc.addWidget(t)

        # ComboBox
        combo_layout = QHBoxLayout()
        combo_layout.setSpacing(15)

        label_pasajero = QLabel("Pasajero #")
        label_pasajero.setFont(QFont("Arial", 16))
        label_pasajero.setStyleSheet("color: white;")

        combo = QComboBox()
        combo.addItems(["Adulto", "Niño", "Adulto Mayor"])
        combo.setMinimumWidth(180)
        combo.setStyleSheet("""
            QComboBox {
                background: white;
                padding: 6px;
                border-radius: 6px;
            }
        """)

        combo_layout.addWidget(label_pasajero)
        combo_layout.addWidget(combo)

        # Botones
        botones = QHBoxLayout()
        botones.setSpacing(20)

        btn_siguiente = QPushButton("Siguiente")
        btn_siguiente.setStyleSheet("""
            QPushButton {
                background: #004C90;
                color: white;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background: #003866;
            }
        """)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background: #FF7A00;
                color: white;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background: #CC6200;
            }
        """)

        botones.addWidget(btn_siguiente)
        botones.addWidget(btn_cancelar)

        # AGREGAR TODO A LA TARJETA
        layout_tarjeta.addWidget(icono, alignment=Qt.AlignCenter)
        layout_tarjeta.addWidget(titulo)
        layout_tarjeta.addSpacing(10)
        layout_tarjeta.addLayout(texto_desc)
        layout_tarjeta.addSpacing(15)
        layout_tarjeta.addLayout(combo_layout)
        layout_tarjeta.addSpacing(25)
        layout_tarjeta.addLayout(botones)

        layout_der.addWidget(tarjeta)

        layout_principal.addWidget(panel_izquierdo, 3)
        layout_principal.addWidget(panel_derecho, 4)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana = VentanaTipoPasajero()
    ventana.show()
    sys.exit(app.exec())