# ventana_registro_pasajero.py
# Nueva ventana con los campos exactos del diseño

from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QLineEdit, QDateEdit, QCalendarWidget
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QPixmap
import recursos_rc


class VentanaRegistroPasajero(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de pasajeros")
        self.resize(1100, 760)

        # ============================
        # LAYOUT PRINCIPAL
        # ============================
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # ============================
        # PANEL IZQUIERDO
        # ============================
        panel_izq = QWidget()
        panel_izq.setStyleSheet("background: white;")
        layout_izq = QVBoxLayout(panel_izq)
        layout_izq.setAlignment(Qt.AlignCenter)

        img = QLabel()
        img.setPixmap(QPixmap(":/recursos/Cartoon-style illust.png").scaled(
            480, 410, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        img.setAlignment(Qt.AlignCenter)

        logo = QLabel()
        logo.setPixmap(QPixmap(":/recursos/Convierte el logo de.png").scaled(
            380, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)

        layout_izq.addWidget(img)
        layout_izq.addWidget(logo)

        # ============================
        # PANEL DERECHO
        # ============================
        panel_der = QWidget()
        panel_der.setStyleSheet("background: #0074B7;")
        layout_der = QVBoxLayout(panel_der)
        layout_der.setAlignment(Qt.AlignCenter)

        # ============================
        # TARJETA INTERNA
        # ============================
        tarjeta = QFrame()
        tarjeta.setStyleSheet("""
            background: #2A9BE7;
            border-radius: 25px;
        """)
        tarjeta.setFixedWidth(420)

        layout_tarjeta = QVBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(40, 20, 40, 30)
        layout_tarjeta.setSpacing(18)

        icono = QLabel()
        icono.setPixmap(QPixmap(":/recursos/logocirculo.png").scaled(
            120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icono.setAlignment(Qt.AlignCenter)

        titulo = QLabel("Registro de\npasajeros")
        titulo.setFont(QFont("Arial", 30, QFont.Bold))
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignCenter)

        # ============================
        # CAMPOS DE TEXTO
        # ============================
        def crear_campo(placeholder):
            campo = QLineEdit()
            campo.setPlaceholderText(placeholder)
            campo.setStyleSheet("""
                QLineEdit {
                    background: white;
                    border-radius: 15px;
                    padding: 10px 15px;
                    font-size: 16px;
                }
            """)
            return campo

        campo_nombre = crear_campo("Nombre")
        campo_ap1 = crear_campo("Primer Apellido")
        campo_ap2 = crear_campo("Segundo Apellido")

        # ============================
        # CAMPO FECHA (MODIFICADO)
        # ============================
        date = QDateEdit()
        date.setCalendarPopup(True)
        date.setDisplayFormat("dd/MM/yyyy")
        date.setDate(QDate.currentDate())  # fecha real del calendario

        # ❗ Hacer que el QDateEdit INICIE VACÍO visualmente
        date.lineEdit().setText("")
        date.setSpecialValueText("")

        # Estilo
        date.setStyleSheet("""
            QDateEdit {
                background-color: white;
                border-radius: 15px;
                padding: 8px 12px;
                font-size: 16px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid #ccc;
                border-radius: 0 15px 15px 0;
            }
            QDateEdit::down-arrow {
                image: url(:/recursos/down-arrow.png);
                width: 14px;
                height: 14px;
            }
        """)

        self.fecha_real = None

        # --- Placeholder superpuesto ---
        placeholder = QLabel("Fecha de nacimiento", date)
        placeholder.setStyleSheet("color:#888; padding-left:5px; font-size:16px; background-color: white;")
        placeholder.move(10, 7)
        placeholder.resize(200, 25)
        placeholder.setAttribute(Qt.WA_TransparentForMouseEvents)
        placeholder.show()

        # --- Eventos para ocultar placeholder ---
        def ocultar_placeholder():
            placeholder.hide()

        date.dateChanged.connect(lambda _: ocultar_placeholder())
        date.calendarWidget().activated.connect(lambda _: ocultar_placeholder())

        # --- QCalendarWidget personalizado ---
        calendar = QCalendarWidget()
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        calendar.setStyleSheet("""
            QCalendarWidget QWidget {
                background-color: #ffffff;
                font-size: 15px;
            }
            QCalendarWidget QToolButton {
                color: #333;
                background-color: #f5f5f5;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #e0e0e0;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #0a79b7;
                selection-color: white;
                font-size: 14px;
            }
        """)
        date.setCalendarWidget(calendar)

        # ============================
        # BOTONES
        # ============================
        botones = QHBoxLayout()
        botones.setSpacing(20)

        btn_siguiente = QPushButton("Siguiente")
        btn_siguiente.setStyleSheet("""
            QPushButton {
                background: #004C90;
                color: white;
                padding: 12px 20px;
                border-radius: 15px;
                font-size: 18px;
            }
            QPushButton:hover { background: #003866; }
        """)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background: #FF7A00;
                color: white;
                padding: 12px 20px;
                border-radius: 15px;
                font-size: 18px;
            }
            QPushButton:hover { background: #CC6200; }
        """)

        botones.addWidget(btn_siguiente)
        botones.addWidget(btn_cancelar)

        # ============================
        # ARMAR TARJETA
        # ============================
        layout_tarjeta.addWidget(icono)
        layout_tarjeta.addWidget(titulo)
        layout_tarjeta.addSpacing(10)
        layout_tarjeta.addWidget(campo_nombre)
        layout_tarjeta.addWidget(campo_ap1)
        layout_tarjeta.addWidget(campo_ap2)
        layout_tarjeta.addWidget(date)
        layout_tarjeta.addSpacing(20)
        layout_tarjeta.addLayout(botones)

        layout_der.addWidget(tarjeta)

        layout_principal.addWidget(panel_izq, 3)
        layout_principal.addWidget(panel_der, 4)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana = VentanaRegistroPasajero()
    ventana.show()
    sys.exit(app.exec())