# ventana_registro_pasajero.py
# Ventana de registro de pasajeros - FUNCIONAL CON BD

from datetime import date
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QLineEdit, QDateEdit, QCalendarWidget, QMessageBox
)
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QFont, QPixmap
from conexion import crear_conexion
import recursos_rc


class VentanaRegistroPasajero(QWidget):
    # Señal que emite el ID del pasajero registrado
    pasajero_registrado = Signal(int)
    
    def __init__(self, numero_pasajero=1, asiento_id=None, total_pasajeros=1):
        super().__init__()
        self.numero_pasajero = numero_pasajero
        self.asiento_id = asiento_id
        self.total_pasajeros = total_pasajeros
        
        self.setWindowTitle(f"Registro de pasajero {numero_pasajero}/{total_pasajeros}")
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
        tarjeta.setFixedWidth(450)

        layout_tarjeta = QVBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(40, 20, 40, 30)
        layout_tarjeta.setSpacing(18)

        icono = QLabel()
        icono.setPixmap(QPixmap(":/recursos/logocirculo.png").scaled(
            120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icono.setAlignment(Qt.AlignCenter)

        # Título dinámico
        titulo = QLabel(f"Pasajero {numero_pasajero}\nde {total_pasajeros}")
        titulo.setFont(QFont("Arial", 28, QFont.Bold))
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignCenter)

        # Info del asiento
        if asiento_id:
            info_asiento = QLabel(f"Asiento: #{asiento_id}")
            info_asiento.setFont(QFont("Arial", 16))
            info_asiento.setStyleSheet("color: #FFD700;")
            info_asiento.setAlignment(Qt.AlignCenter)

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
                    color: black;
                }
            """)
            return campo

        self.campo_nombre = crear_campo("Nombre")
        self.campo_ap1 = crear_campo("Primer Apellido")
        self.campo_ap2 = crear_campo("Segundo Apellido (opcional)")

        # ============================
        # CAMPO FECHA
        # ============================
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDisplayFormat("dd/MM/yyyy")
        self.date.setDate(QDate.currentDate())
        self.date.lineEdit().setText("")
        self.date.setSpecialValueText("")

        self.date.setStyleSheet("""
            QDateEdit {
                background-color: white;
                border-radius: 15px;
                padding: 8px 12px;
                font-size: 16px;
                color: black;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid #ccc;
                border-radius: 0 15px 15px 0;
            }
        """)

        # Placeholder superpuesto
        self.placeholder = QLabel("Fecha de nacimiento", self.date)
        self.placeholder.setStyleSheet("color:#888; padding-left:5px; font-size:16px; background-color: white;")
        self.placeholder.move(10, 7)
        self.placeholder.resize(200, 25)
        self.placeholder.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.placeholder.show()

        def ocultar_placeholder():
            self.placeholder.hide()

        self.date.dateChanged.connect(lambda _: ocultar_placeholder())
        self.date.calendarWidget().activated.connect(lambda _: ocultar_placeholder())

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
        self.date.setCalendarWidget(calendar)

        # ============================
        # BOTONES
        # ============================
        botones = QHBoxLayout()
        botones.setSpacing(20)

        btn_siguiente = QPushButton("Registrar →")
        btn_siguiente.setStyleSheet("""
            QPushButton {
                background: #004C90;
                color: white;
                padding: 12px 20px;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover { background: #003866; }
        """)
        btn_siguiente.clicked.connect(self.registrar_pasajero)

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
        btn_cancelar.clicked.connect(self.cancelar_registro)

        botones.addWidget(btn_siguiente)
        botones.addWidget(btn_cancelar)

        # ============================
        # ARMAR TARJETA
        # ============================
        layout_tarjeta.addWidget(icono)
        layout_tarjeta.addWidget(titulo)
        if asiento_id:
            layout_tarjeta.addWidget(info_asiento)
        layout_tarjeta.addSpacing(10)
        layout_tarjeta.addWidget(self.campo_nombre)
        layout_tarjeta.addWidget(self.campo_ap1)
        layout_tarjeta.addWidget(self.campo_ap2)
        layout_tarjeta.addWidget(self.date)
        layout_tarjeta.addSpacing(20)
        layout_tarjeta.addLayout(botones)

        layout_der.addWidget(tarjeta)

        layout_principal.addWidget(panel_izq, 3)
        layout_principal.addWidget(panel_der, 4)

    def calcular_edad(self, nacimiento):
        """Calcula la edad a partir de la fecha de nacimiento"""
        hoy = date.today()
        edad = hoy.year - nacimiento.year
        if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
            edad -= 1
        return edad

    def registrar_pasajero(self):
        """Registra el pasajero en la base de datos"""
        nombre = self.campo_nombre.text().strip()
        apep = self.campo_ap1.text().strip()
        apem = self.campo_ap2.text().strip()
        
        # Validar que se haya seleccionado fecha
        if self.placeholder.isVisible():
            QMessageBox.warning(self, "Error", "Debes seleccionar una fecha de nacimiento")
            return
        
        nacimiento = self.date.date().toPython()

        # Validaciones
        if not nombre or not apep:
            QMessageBox.warning(self, "Error", "Nombre y apellido paterno son obligatorios")
            return

        edad = self.calcular_edad(nacimiento)

        try:
            conexion = crear_conexion()
            if not conexion:
                QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos")
                return
            
            cursor = conexion.cursor()

            query = """
                INSERT INTO pasajero (paNombre, paPrimerApell, paSegundoApell, fechaNacimiento, edad)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (nombre, apep, apem if apem else None, nacimiento, edad))
            conexion.commit()

            pasajero_id = cursor.lastrowid
            conexion.close()

            # Mensaje de confirmación
            QMessageBox.information(
                self, 
                "Éxito", 
                f"Pasajero {self.numero_pasajero} de {self.total_pasajeros} registrado correctamente\n"
                f"Nombre: {nombre} {apep}\n"
                f"Edad: {edad} años\n"
                f"Asiento: #{self.asiento_id}"
            )
            
            # Emitir señal con el ID del pasajero registrado
            self.pasajero_registrado.emit(pasajero_id)
            
            # Cerrar esta ventana
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el pasajero:\n{e}")
    
    def cancelar_registro(self):
        """Cancela el registro y cierra todo el flujo"""
        respuesta = QMessageBox.question(
            self,
            "Cancelar registro",
            "¿Estás seguro de que deseas cancelar el registro?\n"
            "Se perderán todos los datos ingresados hasta ahora.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            self.close()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana = VentanaRegistroPasajero(numero_pasajero=1, asiento_id=12, total_pasajeros=3)
    ventana.pasajero_registrado.connect(lambda id: print(f"Pasajero registrado con ID: {id}"))
    ventana.show()
    sys.exit(app.exec())