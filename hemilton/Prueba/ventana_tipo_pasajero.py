# ventana_tipo_pasajero.py
# Ventana para seleccionar tipo de pasajero

from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QSizePolicy, QComboBox, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap
from conexion import crear_conexion
import recursos_rc


class VentanaTipoPasajero(QWidget):
    # Señal que emite el número de tipo de pasajero seleccionado
    tipo_seleccionado = Signal(int)
    
    def __init__(self, numero_pasajero=1, asiento_id=None, total_pasajeros=1):
        super().__init__()
        self.numero_pasajero = numero_pasajero
        self.asiento_id = asiento_id
        self.total_pasajeros = total_pasajeros
        self.tipos_disponibles = {}  # {nombre: (id, descuento)}
        
        self.setWindowTitle(f"Tipo de pasajero {numero_pasajero}/{total_pasajeros}")
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
        # CONTENEDOR PRINCIPAL
        # ============================
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # ============================
        # PANEL IZQUIERDO
        # ============================
        panel_izquierdo = QWidget()
        panel_izquierdo.setStyleSheet("background: white;")
        layout_izq = QVBoxLayout(panel_izquierdo)
        layout_izq.setAlignment(Qt.AlignCenter)

        contenedor = QWidget()
        contenedor.setFixedSize(500, 520)

        img = QLabel(contenedor)
        img.setAttribute(Qt.WA_TranslucentBackground)
        img_pix = QPixmap(":/recursos/Cartoon-style illust.png").scaled(
            500, 420, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        img.setPixmap(img_pix)
        img_x = (contenedor.width() - img_pix.width()) // 2
        img.move(img_x, -10)

        logo_bc = QLabel(contenedor)
        logo_bc.setAttribute(Qt.WA_TranslucentBackground)
        logo_pix = QPixmap(":/recursos/Convierte el logo de.png").scaled(
            480, 420, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo_bc.setPixmap(logo_pix)
        logo_x = (contenedor.width() - logo_pix.width()) // 2
        logo_bc.move(logo_x, 250)

        logo_bc.lower()
        img.raise_()

        layout_izq.addWidget(contenedor, alignment=Qt.AlignCenter)

        # ============================
        # PANEL DERECHO
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
        layout_tarjeta.setContentsMargins(40, 20, 40, 30)
        layout_tarjeta.setSpacing(18)

        # Icono
        icono = QLabel()
        icono.setPixmap(QPixmap(":/recursos/logocirculo.png").scaled(
            110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        icono.setAlignment(Qt.AlignCenter)

        # Título dinámico
        titulo = QLabel(f"Pasajero {numero_pasajero}\nde {total_pasajeros}")
        titulo.setFont(QFont("Arial", 30, QFont.Bold))
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignCenter)

        # Info asiento
        if asiento_id:
            info_asiento = QLabel(f"Asiento: #{asiento_id}")
            info_asiento.setFont(QFont("Arial", 16))
            info_asiento.setStyleSheet("color: #FFD700;")
            info_asiento.setAlignment(Qt.AlignCenter)

        # ============================
        # SUBTEXTOS
        # ============================
        texto_desc = QVBoxLayout()
        texto_desc.setSpacing(12)

        t1 = QLabel("Selecciona el tipo de pasajero:")
        t1.setFont(QFont("Arial", 16, QFont.Bold))
        texto_desc.addWidget(t1)

        self.descripcion_tipos = QLabel("")
        self.descripcion_tipos.setFont(QFont("Arial", 13))
        self.descripcion_tipos.setWordWrap(True)
        texto_desc.addWidget(self.descripcion_tipos)

        # ComboBox
        combo_layout = QHBoxLayout()
        combo_layout.setSpacing(15)

        label_tipo = QLabel("Tipo:")
        label_tipo.setFont(QFont("Arial", 16))
        label_tipo.setStyleSheet("color: white;")

        self.combo_tipo = QComboBox()
        self.combo_tipo.setMinimumWidth(220)
        
        combo_layout.addWidget(label_tipo)
        combo_layout.addWidget(self.combo_tipo)

        # Botones
        botones = QHBoxLayout()
        botones.setSpacing(20)

        btn_siguiente = QPushButton("Siguiente →")
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
        btn_siguiente.clicked.connect(self.confirmar_tipo)

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
        btn_cancelar.clicked.connect(self.close)

        botones.addWidget(btn_siguiente)
        botones.addWidget(btn_cancelar)

        # AGREGAR TODO A LA TARJETA
        layout_tarjeta.addWidget(icono, alignment=Qt.AlignCenter)
        layout_tarjeta.addWidget(titulo)
        if asiento_id:
            layout_tarjeta.addWidget(info_asiento)
        layout_tarjeta.addSpacing(10)
        layout_tarjeta.addLayout(texto_desc)
        layout_tarjeta.addSpacing(15)
        layout_tarjeta.addLayout(combo_layout)
        layout_tarjeta.addSpacing(25)
        layout_tarjeta.addLayout(botones)

        layout_der.addWidget(tarjeta)

        layout_principal.addWidget(panel_izquierdo, 3)
        layout_principal.addWidget(panel_derecho, 4)

        # Cargar tipos de pasajero desde BD
        self.cargar_tipos_pasajero()

    def cargar_tipos_pasajero(self):
        """Carga los tipos de pasajero desde la base de datos"""
        try:
            conexion = crear_conexion()
            if not conexion:
                QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos")
                return
            
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT num, descripcion, descuento FROM tipo_pasajero ORDER BY num"
            cursor.execute(query)
            tipos = cursor.fetchall()
            
            descripciones = []
            for tipo in tipos:
                nombre = tipo['descripcion']
                descuento = tipo['descuento']
                tipo_id = tipo['num']
                
                self.tipos_disponibles[nombre] = (tipo_id, descuento)
                self.combo_tipo.addItem(f"{nombre} ({descuento}% desc.)")
                descripciones.append(f"• {nombre}: {descuento}% de descuento")
            
            self.descripcion_tipos.setText("\n".join(descripciones))
            
            cursor.close()
            conexion.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar tipos de pasajero:\n{e}")

    def confirmar_tipo(self):
        """Confirma la selección y emite la señal"""
        if self.combo_tipo.currentIndex() == -1:
            QMessageBox.warning(self, "Error", "Debes seleccionar un tipo de pasajero")
            return
        
        # Extraer nombre del tipo (sin el porcentaje)
        texto_seleccionado = self.combo_tipo.currentText()
        nombre_tipo = texto_seleccionado.split(" (")[0]
        
        if nombre_tipo in self.tipos_disponibles:
            tipo_id, descuento = self.tipos_disponibles[nombre_tipo]
            
            # Emitir señal con el ID del tipo
            self.tipo_seleccionado.emit(tipo_id)
            
            # Cerrar ventana
            self.close()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ventana = VentanaTipoPasajero(numero_pasajero=1, asiento_id=12, total_pasajeros=3)
    ventana.tipo_seleccionado.connect(lambda tipo: print(f"Tipo seleccionado: {tipo}"))
    ventana.show()
    sys.exit(app.exec())