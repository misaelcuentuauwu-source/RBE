from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
)
from PySide6.QtCore import Qt

from conexion import crear_conexion


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

        # El Scroll #
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        contenedor = QWidget()
        vbox = QVBoxLayout(contenedor)

        # Cargar terminales desde la base de datos #
        terminales = self.obtener_terminales()

        # Crear tarjetas #
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
            direccion = QLabel(f"📍 {t['dirCalle']} #{t['dirNumero']}, {t['dirColonia']}")
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

    # Consulta de la BD sobre terminales #
    def obtener_terminales(self):
        try:
            cn = crear_conexion()
            cur = cn.cursor(dictionary=True)

            cur.execute("""
                SELECT 
                    t.nombre as nombre,
                    t.dirCalle as dirCalle,
                    t.dirNumero as dirNumero,
                    t.dirColonia as dirColonia,
                    t.telefono as telefono,
                    c.nombre as ciudad
                FROM terminal as t
                INNER JOIN ciudad as c on c.clave = t.ciudad ;
            """)

            datos = cur.fetchall()
            cur.close()
            cn.close()
            return datos

        except Exception as e:
            print("Error al consultar terminales:", e)
            return []
