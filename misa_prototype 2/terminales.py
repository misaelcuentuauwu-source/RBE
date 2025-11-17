# ventana_terminales.py
import mysql.connector
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QHBoxLayout
)
from PySide6.QtCore import Qt

class VentanaTerminales(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Terminales disponibles")
        self.setGeometry(200, 100, 800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f6f8;
                font-family: 'Segoe UI';
                color: #333;
            }
        """)

        layout = QVBoxLayout(self)

        titulo = QLabel("Terminales disponibles")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 20pt; font-weight: bold; color: #1181c3; margin: 20px;")
        layout.addWidget(titulo)

        # Scroll para mostrar varias terminales
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        contenedor = QWidget()
        vbox = QVBoxLayout(contenedor)

        # Consultar terminales desde la base de datos
        terminales = self.obtener_terminales()

        # Crear “cards” para cada terminal
        for t in terminales:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 10px;
                    margin: 10px;
                    padding: 15px;
                    border: 1px solid #ddd;
                }
                QFrame:hover {
                    border: 1px solid #1181c3;
                }
            """)
            layout_card = QVBoxLayout(card)

            nombre = QLabel(f"🏢 {t['nombre']}")
            nombre.setStyleSheet("font-size: 14pt; font-weight: 600; color: #1181c3;")
            direccion = QLabel(f"📍 {t['calle']} #{t['numero']}, {t['colonia']}")
            telefono = QLabel(f"📞 {t['telefono']}")
            ciudad = QLabel(f"🌆 Ciudad: {t['ciudad']}")

            for lbl in [nombre, direccion, telefono, ciudad]:
                lbl.setStyleSheet("font-size: 11pt; margin: 2px;")

            layout_card.addWidget(nombre)
            layout_card.addWidget(direccion)
            layout_card.addWidget(telefono)
            layout_card.addWidget(ciudad)

            vbox.addWidget(card)

        scroll.setWidget(contenedor)
        layout.addWidget(scroll)

    def obtener_terminales(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="prototipo"
            )
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT ternombre AS nombre, telefono, tercalle AS calle, ternumero AS numero, tercolonia AS colonia, ciudad FROM terminal;")
            datos = cursor.fetchall()
            conexion.close()
            return datos
        except Exception as e:
            print("Error al conectar o consultar:", e)
            return []
