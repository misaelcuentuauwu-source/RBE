# ventana_generar_boletos.py - Versión final optimizada
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QScrollArea, QFileDialog, QMessageBox,
    QColorDialog, QButtonGroup, QRadioButton
)
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QImage, QRegion, QPageSize
from PySide6.QtPrintSupport import QPrinter
from conexion import crear_conexion

class TicketCanvas(QFrame):
    """Widget que dibuja el boleto personalizado"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(760, 280)
        self.setMaximumSize(760, 280)

        # Datos del boleto (valores por defecto)
        self.numero_boleto = "000000000"
        self.origen = "Origen"
        self.destino = "Destino"
        self.fecha_salida = "01/01/2025 00:00"
        self.asiento = "00"
        self.pasajero = "Nombre Pasajero"
        self.precio = "$0.00"
        self.tipo_pasajero = "Regular"

        # Colores personalizables
        self.color_primario = QColor("#0074B7")
        self.color_secundario = QColor("#FFFFFF")
        self.color_texto = QColor("#000000")
        self.color_acento = QColor("#E86A1E")

        self.setStyleSheet("background: white; border: 2px solid #ccc; border-radius: 8px;")

    def set_datos(self, datos):
        """Actualiza los datos del boleto"""
        self.numero_boleto = datos.get('numero_boleto', '000000000')
        self.origen = datos.get('origen', 'Origen')
        self.destino = datos.get('destino', 'Destino')
        self.fecha_salida = datos.get('fecha_salida', '01/01/2025 00:00')
        self.asiento = str(datos.get('asiento', '00'))
        self.pasajero = datos.get('pasajero', 'Nombre Pasajero')
        self.precio = datos.get('precio', '$0.00')
        self.tipo_pasajero = datos.get('tipo_pasajero', 'Regular')
        self.update()

    def set_colores(self, primario, secundario, texto, acento):
        """Actualiza los colores del boleto"""
        self.color_primario = QColor(primario)
        self.color_secundario = QColor(secundario)
        self.color_texto = QColor(texto)
        self.color_acento = QColor(acento)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        margen = 20

        # PARTE IZQUIERDA
        izq_w = w // 2

        # Cabecera
        painter.fillRect(0, 0, izq_w, 80, self.color_primario)

        # Logo autobús
        painter.setPen(QPen(self.color_secundario, 3))
        painter.setBrush(self.color_secundario)
        bus_x, bus_y = 30, 20
        painter.drawRoundedRect(bus_x, bus_y, 50, 40, 5, 5)
        painter.fillRect(bus_x+10, bus_y+8, 12, 10, self.color_primario)
        painter.fillRect(bus_x+28, bus_y+8, 12, 10, self.color_primario)

        # Título
        painter.setPen(self.color_secundario)
        painter.setFont(QFont("Arial", 18, QFont.Bold))
        painter.drawText(QRect(100, 15, 300, 30), Qt.AlignLeft, "RUTAS BAJA EXPRESS")

        painter.setFont(QFont("Courier", 12, QFont.Bold))
        painter.drawText(QRect(100, 45, 300, 25), Qt.AlignLeft, "★ RBE ★")
        painter.setFont(QFont("Courier", 14, QFont.Bold))
        painter.drawText(QRect(100, 60, 300, 25), Qt.AlignLeft, self.numero_boleto)

        # Origen y Destino
        y_offset = 100
        painter.setPen(self.color_texto)
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(QRect(margen, y_offset, 150, 20), Qt.AlignLeft, "ORIGEN:")
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(QRect(margen, y_offset+20, 200, 30), Qt.AlignLeft, self.origen)

        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(QRect(izq_w-170, y_offset, 150, 20), Qt.AlignRight, "DESTINO:")
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(QRect(izq_w-200, y_offset+20, 200, 30), Qt.AlignRight, self.destino)

        y_offset += 60

        # Fecha
        painter.setPen(self.color_texto)
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(QRect(margen, y_offset, 200, 20), Qt.AlignLeft, "FECHA Y HORA:")
        painter.setFont(QFont("Arial", 12))
        painter.drawText(QRect(margen, y_offset+20, 200, 25), Qt.AlignLeft, self.fecha_salida)

        y_offset += 50

        # Asiento
        painter.setPen(self.color_acento)
        painter.setBrush(self.color_acento)
        painter.drawRoundedRect(margen, y_offset, 100, 45, 8, 8)
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(QRect(margen, y_offset+5, 100, 20), Qt.AlignCenter, "ASIENTO")
        painter.setFont(QFont("Arial", 20, QFont.Bold))
        painter.drawText(QRect(margen, y_offset+20, 100, 25), Qt.AlignCenter, self.asiento)

        # Precio
        painter.setPen(self.color_primario)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(margen+120, y_offset, 120, 45, 8, 8)
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(QRect(margen+120, y_offset+5, 120, 20), Qt.AlignCenter, "PRECIO")
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(QRect(margen+120, y_offset+20, 120, 25), Qt.AlignCenter, self.precio)

        # PARTE DERECHA (Talón)
        der_x = w // 2
        der_w = w // 2

        painter.fillRect(der_x, 0, der_w, h, QColor("#F5F5F5"))
        painter.fillRect(der_x, 0, der_w, 80, self.color_primario)

        # Logo pequeño
        painter.setPen(QPen(self.color_secundario, 2))
        painter.setBrush(self.color_secundario)
        bus_x2, bus_y2 = der_x + 20, 25
        painter.drawRoundedRect(bus_x2, bus_y2, 40, 30, 4, 4)
        painter.fillRect(bus_x2+8, bus_y2+6, 10, 8, self.color_primario)
        painter.fillRect(bus_x2+22, bus_y2+6, 10, 8, self.color_primario)

        painter.setPen(self.color_secundario)
        painter.setFont(QFont("Courier", 10, QFont.Bold))
        painter.drawText(QRect(der_x+70, 20, 200, 20), Qt.AlignLeft, "★ RBE ★")
        painter.setFont(QFont("Courier", 12, QFont.Bold))
        painter.drawText(QRect(der_x+70, 40, 200, 25), Qt.AlignLeft, self.numero_boleto)

        # Info talón
        y_talon = 100
        painter.setPen(self.color_texto)

        painter.setFont(QFont("Arial", 9, QFont.Bold))
        painter.drawText(QRect(der_x+15, y_talon, der_w-30, 20), Qt.AlignLeft, "PASAJERO:")
        painter.setFont(QFont("Arial", 11))
        painter.drawText(QRect(der_x+15, y_talon+18, der_w-30, 25), Qt.AlignLeft, self.pasajero)

        y_talon += 50

        painter.setFont(QFont("Arial", 9, QFont.Bold))
        painter.drawText(QRect(der_x+15, y_talon, der_w-30, 20), Qt.AlignLeft, "TIPO:")
        painter.setFont(QFont("Arial", 11))
        painter.drawText(QRect(der_x+15, y_talon+18, der_w-30, 25), Qt.AlignLeft, self.tipo_pasajero)

        y_talon += 50

        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.setPen(self.color_acento)
        painter.drawText(QRect(der_x+15, y_talon, der_w-30, 30), Qt.AlignCenter,
                        f"{self.origen} → {self.destino}")

        y_talon += 40

        painter.setPen(self.color_primario)
        painter.setBrush(self.color_primario)
        painter.drawRoundedRect(der_x+30, y_talon, 80, 35, 6, 6)
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        painter.drawText(QRect(der_x+30, y_talon+3, 80, 15), Qt.AlignCenter, "ASIENTO")
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(QRect(der_x+30, y_talon+15, 80, 20), Qt.AlignCenter, self.asiento)

        # Código de barras simulado
        painter.setPen(self.color_texto)
        for i in range(30):
            x = der_x + 130 + i*3
            altura = 20 if i % 3 == 0 else 30
            painter.drawLine(x, y_talon+5, x, y_talon+altura)

        painter.end()

    def exportar_imagen(self):
        """Exporta el boleto como imagen (PNG)"""
        image = QImage(self.size(), QImage.Format_ARGB32)
        image.fill(Qt.white)

        painter = QPainter(image)
        self.render(painter, QPoint(0, 0), QRegion(), QWidget.RenderFlags(QWidget.RenderFlag.DrawChildren))
        painter.end()

        return image

class VentanaGenerarBoletos(QWidget):
    def __init__(self, pasajeros_info=None, id_viaje=None):
        super().__init__()

        # Validación inicial
        if not pasajeros_info or id_viaje is None:
            QMessageBox.critical(self, "Error", "Datos de pasajeros o ID de viaje no proporcionados.")
            self.close()
            return

        self.pasajeros_info = pasajeros_info
        self.id_viaje = id_viaje
        self.indice_actual = 0
        self.datos_viaje = {}

        # Diccionario para almacenar colores personalizados por pasajero
        self.colores_pasajeros = {}

        self.setWindowTitle("Generar Boletos - Rutas Baja Express")
        self.resize(1400, 800)

        # LAYOUT PRINCIPAL
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # ===== PANEL IZQUIERDO - Plantillas =====
        panel_izq = QFrame()
        panel_izq.setStyleSheet("background: #1a1a1a;")
        panel_izq.setFixedWidth(350)

        layout_izq = QVBoxLayout(panel_izq)
        layout_izq.setContentsMargins(15, 15, 15, 15)
        layout_izq.setSpacing(15)

        # Título
        titulo_panel = QLabel("Personalización")
        titulo_panel.setFont(QFont("Arial", 20, QFont.Bold))
        titulo_panel.setStyleSheet("color: white;")
        layout_izq.addWidget(titulo_panel)

        # Selector de pasajero
        lbl_pasajero = QLabel("Pasajero:")
        lbl_pasajero.setStyleSheet("color: white; font-size: 14px;")
        layout_izq.addWidget(lbl_pasajero)

        nav_pasajero = QHBoxLayout()

        self.btn_anterior = QPushButton("◄")
        self.btn_anterior.setFixedSize(40, 40)
        self.btn_anterior.setStyleSheet("""
            QPushButton {
                background: #0074B7;
                color: white;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover { background: #005a8f; }
            QPushButton:disabled { background: #444; color: #888; }
        """)
        self.btn_anterior.clicked.connect(self.pasajero_anterior)

        self.lbl_contador = QLabel(f"1 / {len(self.pasajeros_info)}")
        self.lbl_contador.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.lbl_contador.setAlignment(Qt.AlignCenter)

        self.btn_siguiente = QPushButton("►")
        self.btn_siguiente.setFixedSize(40, 40)
        self.btn_siguiente.setStyleSheet("""
            QPushButton {
                background: #0074B7;
                color: white;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover { background: #005a8f; }
            QPushButton:disabled { background: #444; color: #888; }
        """)
        self.btn_siguiente.clicked.connect(self.pasajero_siguiente)

        nav_pasajero.addWidget(self.btn_anterior)
        nav_pasajero.addWidget(self.lbl_contador, stretch=1)
        nav_pasajero.addWidget(self.btn_siguiente)
        layout_izq.addLayout(nav_pasajero)

        # Scroll para plantillas
        scroll_plantillas = QScrollArea()
        scroll_plantillas.setWidgetResizable(True)
        scroll_plantillas.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #0074B7;
                border-radius: 5px;
            }
        """)

        contenedor_plantillas = QWidget()
        layout_plantillas = QVBoxLayout(contenedor_plantillas)
        layout_plantillas.setSpacing(12)

        # Plantillas predefinidas con buen contraste
        lbl_plantillas = QLabel("Plantillas")
        lbl_plantillas.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout_plantillas.addWidget(lbl_plantillas)

        self.grupo_plantillas = QButtonGroup()

        plantillas = [
            ("Clásico Azul", "#0074B7", "#FFFFFF", "#000000", "#E86A1E"),
            ("Profesional", "#2C3E50", "#ECF0F1", "#2C3E50", "#3498DB"),
            ("Verde Fresco", "#27AE60", "#FFFFFF", "#2C3E50", "#E74C3C"),
            ("Morado Elegante", "#8E44AD", "#FFFFFF", "#2C3E50", "#F1C40F"),
            ("Naranja Vibrante", "#E67E22", "#FFFFFF", "#2C3E50", "#2980B9"),
            ("Minimalista", "#FFFFFF", "#2C3E50", "#2C3E50", "#3498DB"),
            ("Oscuro Moderno", "#1A1A1A", "#FFFFFF", "#FFFFFF", "#3498DB"),
            ("Azul Claro", "#3498DB", "#FFFFFF", "#2C3E50", "#E74C3C"),
        ]

        for i, (nombre, primario, secundario, texto, acento) in enumerate(plantillas):
            plantilla_btn = self.crear_boton_plantilla(nombre, primario, secundario, texto, acento)
            self.grupo_plantillas.addButton(plantilla_btn, i)
            layout_plantillas.addWidget(plantilla_btn)

        # Seleccionar primera plantilla
        self.grupo_plantillas.button(0).setChecked(True)

        layout_plantillas.addSpacing(20)

        # Colores personalizados
        lbl_colores = QLabel("Colores Personalizados")
        lbl_colores.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout_plantillas.addWidget(lbl_colores)

        self.colores_custom = {}
        colores_config = [
            ("Color Primario", "primario"),
            ("Color Secundario", "secundario"),
            ("Color Texto", "texto"),
            ("Color Acento", "acento")
        ]

        for nombre, key in colores_config:
            btn_color = self.crear_selector_color(nombre, key)
            layout_plantillas.addWidget(btn_color)

        layout_plantillas.addStretch()

        scroll_plantillas.setWidget(contenedor_plantillas)
        layout_izq.addWidget(scroll_plantillas, stretch=1)

        # ===== PANEL CENTRAL - Vista previa =====
        panel_centro = QFrame()
        panel_centro.setStyleSheet("background: #f0f0f0;")

        layout_centro = QVBoxLayout(panel_centro)
        layout_centro.setAlignment(Qt.AlignCenter)
        layout_centro.setContentsMargins(20, 20, 20, 20)

        titulo_vista = QLabel("Vista Previa del Boleto")
        titulo_vista.setFont(QFont("Arial", 22, QFont.Bold))
        titulo_vista.setStyleSheet("color: #333;")
        titulo_vista.setAlignment(Qt.AlignCenter)
        layout_centro.addWidget(titulo_vista)

        layout_centro.addSpacing(20)

        # Canvas del boleto
        self.ticket_canvas = TicketCanvas()
        layout_centro.addWidget(self.ticket_canvas, alignment=Qt.AlignCenter)

        layout_centro.addSpacing(30)

        # Botones de exportación
        botones_accion = QHBoxLayout()
        botones_accion.setSpacing(15)

        btn_exportar_png = QPushButton("📄 Exportar como PNG")
        btn_exportar_png.setFixedHeight(50)
        btn_exportar_png.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover { background: #45a049; }
        """)
        btn_exportar_png.clicked.connect(lambda: self.exportar_boleto("PNG"))

        btn_exportar_pdf = QPushButton("📑 Exportar como PDF")
        btn_exportar_pdf.setFixedHeight(50)
        btn_exportar_pdf.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover { background: #1976D2; }
        """)
        btn_exportar_pdf.clicked.connect(lambda: self.exportar_boleto("PDF"))

        botones_accion.addWidget(btn_exportar_png)
        botones_accion.addWidget(btn_exportar_pdf)

        layout_centro.addLayout(botones_accion)

        # ===== PANEL DERECHO - Opciones =====
        panel_der = QFrame()
        panel_der.setStyleSheet("background: white; border-left: 2px solid #ccc;")
        panel_der.setFixedWidth(300)

        layout_der = QVBoxLayout(panel_der)
        layout_der.setContentsMargins(20, 20, 20, 20)
        layout_der.setSpacing(20)

        titulo_opciones = QLabel("Opciones de Exportación")
        titulo_opciones.setFont(QFont("Arial", 18, QFont.Bold))
        titulo_opciones.setStyleSheet("color: #333;")
        layout_der.addWidget(titulo_opciones)

        # Exportar todos
        btn_exportar_todos = QPushButton("📦 Exportar Todos los Boletos")
        btn_exportar_todos.setFixedHeight(60)
        btn_exportar_todos.setStyleSheet("""
            QPushButton {
                background: #FF9800;
                color: white;
                border-radius: 12px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover { background: #F57C00; }
        """)
        btn_exportar_todos.clicked.connect(self.exportar_todos)
        layout_der.addWidget(btn_exportar_todos)

        # Info del viaje
        frame_info = QFrame()
        frame_info.setStyleSheet("background: #E3F2FD; border-radius: 10px; padding: 15px;")
        layout_info = QVBoxLayout(frame_info)

        self.lbl_info_viaje = QLabel()
        self.lbl_info_viaje.setStyleSheet("color: #1565C0; font-size: 13px;")
        self.lbl_info_viaje.setWordWrap(True)
        layout_info.addWidget(self.lbl_info_viaje)

        layout_der.addWidget(frame_info)

        # Info del pasajero
        frame_pasajero = QFrame()
        frame_pasajero.setStyleSheet("background: #FFF3E0; border-radius: 10px; padding: 15px;")
        layout_pax = QVBoxLayout(frame_pasajero)

        self.lbl_info_pasajero = QLabel()
        self.lbl_info_pasajero.setStyleSheet("color: #E65100; font-size: 13px;")
        self.lbl_info_pasajero.setWordWrap(True)
        layout_pax.addWidget(self.lbl_info_pasajero)

        layout_der.addWidget(frame_pasajero)

        layout_der.addStretch()

        # Botón cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setFixedHeight(45)
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background: #f44336;
                color: white;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover { background: #da190b; }
        """)
        btn_cerrar.clicked.connect(self.close)
        layout_der.addWidget(btn_cerrar)

        # AGREGAR PANELES
        layout_principal.addWidget(panel_izq)
        layout_principal.addWidget(panel_centro, stretch=1)
        layout_principal.addWidget(panel_der)

        # Cargar datos y actualizar vista
        self.cargar_datos_viaje()
        self.actualizar_vista_boleto()
        self.actualizar_botones_navegacion()

    def crear_boton_plantilla(self, nombre, primario, secundario, texto, acento):
        """Crea un botón de plantilla con vista previa"""
        btn = QRadioButton()
        btn.setFixedHeight(70)
        btn.setStyleSheet(f"""
            QRadioButton {{
                background: #2a2a2a;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }}
            QRadioButton:hover {{
                background: #3a3a3a;
            }}
            QRadioButton:checked {{
                background: {primario};
                border: 3px solid {acento};
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #666;
                background: #1a1a1a;
            }}
            QRadioButton::indicator:checked {{
                background: {acento};
                border: 2px solid white;
            }}
        """)

        btn.setText(f"  {nombre}")
        btn.clicked.connect(lambda: self.aplicar_plantilla(primario, secundario, texto, acento))

        return btn

    def crear_selector_color(self, nombre, key):
        """Crea un selector de color personalizado"""
        container = QFrame()
        container.setStyleSheet("background: #2a2a2a; border-radius: 8px; padding: 8px;")

        layout = QHBoxLayout(container)
        layout.setContentsMargins(10, 5, 10, 5)

        lbl = QLabel(nombre)
        lbl.setStyleSheet("color: white; font-size: 13px;")

        btn_color = QPushButton("Elegir")
        btn_color.setFixedSize(70, 30)
        btn_color.setStyleSheet("""
            QPushButton {
                background: #0074B7;
                color: white;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover { background: #005a8f; }
        """)
        btn_color.clicked.connect(lambda: self.elegir_color(key))

        self.colores_custom[key] = "#0074B7"

        layout.addWidget(lbl)
        layout.addStretch()
        layout.addWidget(btn_color)

        return container

    def elegir_color(self, key):
        """Abre el selector de color"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.colores_custom[key] = color.name()
            self.aplicar_colores_custom()

    def aplicar_plantilla(self, primario, secundario, texto, acento):
        """Aplica una plantilla predefinida al boleto actual"""
        pasajero_id = self.pasajeros_info[self.indice_actual]['pasajero_id']
        self.colores_pasajeros[pasajero_id] = {
            'primario': primario,
            'secundario': secundario,
            'texto': texto,
            'acento': acento
        }
        self.ticket_canvas.set_colores(primario, secundario, texto, acento)

    def aplicar_colores_custom(self):
        """Aplica colores personalizados al boleto actual"""
        if len(self.colores_custom) == 4:
            pasajero_id = self.pasajeros_info[self.indice_actual]['pasajero_id']
            self.colores_pasajeros[pasajero_id] = {
                'primario': self.colores_custom['primario'],
                'secundario': self.colores_custom['secundario'],
                'texto': self.colores_custom['texto'],
                'acento': self.colores_custom['acento']
            }
            self.ticket_canvas.set_colores(
                self.colores_custom['primario'],
                self.colores_custom['secundario'],
                self.colores_custom['texto'],
                self.colores_custom['acento']
            )

    def cargar_datos_viaje(self):
        """Carga información del viaje desde la base de datos"""
        if not self.id_viaje:
            QMessageBox.warning(self, "Error", "ID de viaje no proporcionado.")
            return

        try:
            conn = crear_conexion()
            if not conn:
                return

            cursor = conn.cursor(dictionary=True)

            query = """
            SELECT
                v.numero AS viaje_id,
                v.fecHoraSalida,
                t_origen.nombre AS origen,
                t_destino.nombre AS destino,
                r.precio AS precio_base
            FROM viaje v
            JOIN ruta r ON v.ruta = r.codigo
            JOIN terminal t_origen ON r.origen = t_origen.numero
            JOIN terminal t_destino ON r.destino = t_destino.numero
            WHERE v.numero = %s
            """
            cursor.execute(query, (self.id_viaje,))
            viaje = cursor.fetchone()

            if viaje:
                self.datos_viaje = {
                    'numero': viaje['viaje_id'],
                    'origen': viaje['origen'],
                    'destino': viaje['destino'],
                    'fecha_salida': viaje['fecHoraSalida'].strftime('%d/%m/%Y %H:%M'),
                    'precio_base': float(viaje['precio_base'])
                }

                self.lbl_info_viaje.setText(
                    f"<b>Viaje #{viaje['viaje_id']}</b><br>"
                    f"Ruta: {viaje['origen']} → {viaje['destino']}<br>"
                    f"Salida: {viaje['fecHoraSalida'].strftime('%d/%m/%Y %H:%M')}<br>"
                    f"Precio base: ${viaje['precio_base']:.2f}"
                )
            else:
                QMessageBox.warning(self, "Error", "No se encontró el viaje especificado.")

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos del viaje:\n{str(e)}")

    def actualizar_vista_boleto(self):
        """Actualiza el canvas con los datos del pasajero actual"""
        if not self.pasajeros_info or self.indice_actual >= len(self.pasajeros_info):
            return

        try:
            info = self.pasajeros_info[self.indice_actual]

            conn = crear_conexion()
            if not conn:
                return

            cursor = conn.cursor(dictionary=True)

            query_pax = """
            SELECT
                paNombre, paPrimerApell, paSegundoApell
            FROM pasajero
            WHERE num = %s
            """
            cursor.execute(query_pax, (info['pasajero_id'],))
            pax = cursor.fetchone()

            query_tipo = """
            SELECT
                descripcion, descuento
            FROM tipo_pasajero
            WHERE num = %s
            """
            cursor.execute(query_tipo, (info['tipo_pasajero'],))
            tipo = cursor.fetchone()

            if pax and tipo:
                nombre_completo = f"{pax['paNombre']} {pax['paPrimerApell']}"
                if pax['paSegundoApell']:
                    nombre_completo += f" {pax['paSegundoApell']}"

                numero_boleto = f"{self.id_viaje}{info['asiento_id']:03d}{info['pasajero_id']:04d}"

                descuento = tipo['descuento']
                precio_final = self.datos_viaje['precio_base'] * (1 - descuento / 100.0)

                datos_boleto = {
                    'numero_boleto': numero_boleto,
                    'origen': self.datos_viaje.get('origen', 'Origen'),
                    'destino': self.datos_viaje.get('destino', 'Destino'),
                    'fecha_salida': self.datos_viaje.get('fecha_salida', '01/01/2025 00:00'),
                    'asiento': str(info['asiento_id']),
                    'pasajero': nombre_completo,
                    'precio': f"${precio_final:.2f}",
                    'tipo_pasajero': tipo['descripcion']
                }

                self.ticket_canvas.set_datos(datos_boleto)

                pasajero_id = info['pasajero_id']
                if pasajero_id in self.colores_pasajeros:
                    colores = self.colores_pasajeros[pasajero_id]
                    self.ticket_canvas.set_colores(
                        colores['primario'],
                        colores['secundario'],
                        colores['texto'],
                        colores['acento']
                    )

                self.lbl_info_pasajero.setText(
                    f"<b>{nombre_completo}</b><br>"
                    f"Asiento: #{info['asiento_id']}<br>"
                    f"Tipo: {tipo['descripcion']} (-{descuento}%)<br>"
                    f"Precio: ${precio_final:.2f}"
                )

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al actualizar vista:\n{str(e)}")

    def pasajero_anterior(self):
        """Navega al pasajero anterior"""
        if self.indice_actual > 0:
            self.indice_actual -= 1
            self.actualizar_vista_boleto()
            self.actualizar_botones_navegacion()

    def pasajero_siguiente(self):
        """Navega al siguiente pasajero"""
        if self.indice_actual < len(self.pasajeros_info) - 1:
            self.indice_actual += 1
            self.actualizar_vista_boleto()
            self.actualizar_botones_navegacion()

    def actualizar_botones_navegacion(self):
        """Actualiza el estado de los botones de navegación"""
        self.btn_anterior.setEnabled(self.indice_actual > 0)
        self.btn_siguiente.setEnabled(self.indice_actual < len(self.pasajeros_info) - 1)
        self.lbl_contador.setText(f"{self.indice_actual + 1} / {len(self.pasajeros_info)}")

    def exportar_boleto(self, formato):
        """Exporta el boleto actual como PNG o PDF"""
        if formato == "PNG":
            archivo, _ = QFileDialog.getSaveFileName(
                self, "Guardar boleto",
                f"Boleto_{self.indice_actual + 1}.png",
                "PNG (*.png)"
            )
            if archivo:
                try:
                    image = self.ticket_canvas.exportar_imagen()
                    if image.save(archivo):
                        QMessageBox.information(self, "Éxito", f"Boleto guardado en:\n{archivo}")
                    else:
                        QMessageBox.critical(self, "Error", "No se pudo guardar el archivo PNG.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al exportar PNG:\n{str(e)}")

        elif formato == "PDF":
            archivo, _ = QFileDialog.getSaveFileName(
                self, "Guardar boleto",
                f"Boleto_{self.indice_actual + 1}.pdf",
                "PDF (*.pdf)"
            )
            if archivo:
                try:
                    printer = QPrinter(QPrinter.HighResolution)
                    printer.setOutputFormat(QPrinter.PdfFormat)
                    printer.setOutputFileName(archivo)
                    printer.setPageSize(QPageSize(QPageSize.A4))

                    painter = QPainter(printer)
                    page_rect = printer.pageRect(QPrinter.DevicePixel)
                    scale = min(
                        page_rect.width() / self.ticket_canvas.width(),
                        page_rect.height() / self.ticket_canvas.height()
                    ) * 0.8
                    painter.scale(scale, scale)
                    self.ticket_canvas.render(painter, QPoint(0, 0))
                    painter.end()

                    QMessageBox.information(self, "Éxito", f"Boleto guardado en:\n{archivo}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al exportar PDF:\n{str(e)}")

    def exportar_todos(self):
        """Exporta todos los boletos como PNG y PDF"""
        import os

        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de destino")
        if not carpeta:
            return

        try:
            for i in range(len(self.pasajeros_info)):
                self.indice_actual = i
                self.actualizar_vista_boleto()

                # Exportar PNG
                archivo_png = os.path.join(carpeta, f"Boleto_{i + 1}.png")
                image = self.ticket_canvas.exportar_imagen()
                image.save(archivo_png)

                # Exportar PDF
                archivo_pdf = os.path.join(carpeta, f"Boleto_{i + 1}.pdf")
                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(archivo_pdf)
                printer.setPageSize(QPageSize(QPageSize.A4))

                painter = QPainter(printer)
                page_rect = printer.pageRect(QPrinter.DevicePixel)
                scale = min(
                    page_rect.width() / self.ticket_canvas.width(),
                    page_rect.height() / self.ticket_canvas.height()
                ) * 0.8
                painter.scale(scale, scale)
                self.ticket_canvas.render(painter, QPoint(0, 0))
                painter.end()

            self.indice_actual = 0
            self.actualizar_vista_boleto()
            self.actualizar_botones_navegacion()

            QMessageBox.information(
                self, "Éxito",
                f"Se exportaron {len(self.pasajeros_info)} boletos en:\n{carpeta}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar boletos:\n{str(e)}")

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    pasajeros_prueba = [
        {'pasajero_id': 1, 'asiento_id': 12, 'tipo_pasajero': 1},
        {'pasajero_id': 2, 'asiento_id': 13, 'tipo_pasajero': 2}
    ]

    ventana = VentanaGenerarBoletos(pasajeros_info=pasajeros_prueba, id_viaje=1)
    ventana.show()
    sys.exit(app.exec())