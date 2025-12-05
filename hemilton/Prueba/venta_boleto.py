from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QApplication, QPushButton, QHBoxLayout, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import sys
from conexion import crear_conexion
from seleccionar_asiento import SeleccionarAsiento


#clase principal#

class SeleccionarViaje(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RBE - Seleccionar Viaje")
        self.setMinimumSize(650, 500)
        self.setStyleSheet(self.estilos())

        layout = QVBoxLayout(self)

        # Titulo #
        titulo = QLabel("Seleccionar Viaje")
        titulo.setFont(QFont("Arial", 22, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo")

        layout.addWidget(titulo)

        # Lista de los viajes #
        self.lista_viajes = QListWidget()
        self.lista_viajes.setObjectName("listaViajes")
        self.cargar_viajes()

        layout.addWidget(self.lista_viajes)

        # Botones #
        btn_layout = QHBoxLayout()

        self.btn_seleccionar = QPushButton("Continuar →")
        self.btn_seleccionar.setObjectName("botonPrincipal")
        self.btn_seleccionar.clicked.connect(self.abrir_asientos)  # conecta acción

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_seleccionar)

        layout.addLayout(btn_layout)

    # Consulta de los viajes #
    def cargar_viajes(self):
        db = crear_conexion()
        cursor = db.cursor()

        cursor.execute("""
            SELECT v.numero, t1.nombre AS origen, t2.nombre AS destino,
                   v.fecHoraSalida, v.fecHoraEntrada
            FROM viaje v
            JOIN ruta r ON v.ruta = r.codigo
            JOIN terminal t1 ON r.origen = t1.numero
            JOIN terminal t2 ON r.destino = t2.numero
            ORDER BY v.fecHoraSalida
        """)

        for id_viaje, origen, destino, salida, entrada in cursor.fetchall():
            texto = f"Viaje {id_viaje} – {origen} → {destino} – {salida.strftime('%Y-%m-%d %H:%M')}"
            item = QListWidgetItem(texto)
            item.setData(Qt.UserRole, id_viaje)
            self.lista_viajes.addItem(item)

        db.close()

    # En caso de que haga algo mal #
    def abrir_asientos(self):
        item = self.lista_viajes.currentItem()
        if not item:
            QMessageBox.warning(self, "Aviso", "Selecciona un viaje primero.")
            return

        id_viaje = item.data(Qt.UserRole)
        # Abrimos la ventana de asientos #
        self.ventana_asientos = SeleccionarAsiento(id_viaje)
        self.ventana_asientos.show()

    # Style #
    def estilos(self):
        return """
        #titulo {
            color: #333;
        }

        #listaViajes {
            background: #f0f0f0;
            padding: 10px;
            border-radius: 10px;
            font-size: 15px;
        }

        QListWidget::item {
            padding: 12px;
            background: white;
            border-radius: 8px;
            margin-bottom: 8px;
        }

        QListWidget::item:selected {
            background: #0078ff;
            color: white;
        }

        #botonPrincipal {
            background-color: #0078ff;
            color: white;
            padding: 10px 20px;
            border-radius: 12px;
            font-size: 16px;
        }
        #botonPrincipal:hover {
            background-color: #005fcc;
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SeleccionarViaje()
    ventana.show()
    sys.exit(app.exec())
