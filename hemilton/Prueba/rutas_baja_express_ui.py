import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QScrollArea, QDateEdit,
    QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt, QRect, QSize, QPoint, QDate
from PySide6.QtGui import QFont, QPixmap

from conexion import crear_conexion
from ventana_asientosxd import VentanaAsientos

import recursos_rc  

## Flotante para cambiar de pantalla y no de ventana ##
class FlowLayout(__import__('PySide6.QtWidgets', fromlist=['QLayout']).QLayout):
    def __init__(self, parent=None, margin=0, spacing=24):
        super().__init__(parent)
        self._items = []
        self.setSpacing(spacing)
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item):
        self._items.append(item)

    def addWidget(self, widget):
        self.addChildWidget(widget)
        self.addItem(widget)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        from PySide6.QtWidgets import QWidgetItem
        if 0 <= index < len(self._items):
            it = self._items[index]
            if isinstance(it, QWidget):
                return QWidgetItem(it)
            return it
        return None

    def takeAt(self, index):
        from PySide6.QtWidgets import QWidgetItem
        if 0 <= index < len(self._items):
            it = self._items.pop(index)
            if isinstance(it, QWidget):
                return QWidgetItem(it)
            return it
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            hint = item.sizeHint() if hasattr(item, "sizeHint") else item.widget().sizeHint()
            size = size.expandedTo(hint)
        l, t, r, b = self.getContentsMargins()
        size += QSize(l + r, t + b)
        return size

    def doLayout(self, rect, test):
        x = rect.x()
        y = rect.y()
        lineH = 0
        left, top, right, bottom = self.getContentsMargins()
        x += left
        y += top
        maxW = rect.width() - (left + right)

        for item in self._items:
            widget = item if isinstance(item, QWidget) else item.widget()
            hint = widget.sizeHint()
            w, h = hint.width(), hint.height()

            if x + w > rect.x() + maxW and x > rect.x() + left:
                x = rect.x() + left
                y += lineH + self.spacing()
                lineH = 0

            if not test:
                widget.setGeometry(QRect(QPoint(x, y), QSize(w, h)))

            x += w + self.spacing()
            lineH = max(lineH, h)

        return y + lineH + bottom

## Main ##
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rutas Baja Express")
        self.resize(1100, 760)

        self.setStyleSheet("""
        QComboBox, QDateEdit {
            background: white;
            border: 2px solid #cccccc;
            border-radius: 10px;
            padding: 6px 10px;
            font-size: 14px;
            min-width: 150px;
        }
        QComboBox::drop-down, QDateEdit::drop-down { border: none; width: 28px; }
        QComboBox::down-arrow { image: url(:/icons/down.svg); width:14px;height:14px; }
        QDateEdit::down-arrow { image: url(:/icons/calendar.svg); width:14px;height:14px; }
        QComboBox:hover, QDateEdit:hover { border:2px solid #aaaaaa; }
        
        QCheckBox {
            color: #333;
            font-size: 13px;
            font-weight: 500;
        }
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 2px solid #cccccc;
            background: white;
        }
        QCheckBox::indicator:checked {
            background: #0a79b7;
            border: 2px solid #0a79b7;
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEzLjMzMzMgNC42NjY2N0w2LjAwMDAwIDEyTDIuNjY2NjcgOC42NjY2NyIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
        }
        QCheckBox::indicator:hover {
            border: 2px solid #0a79b7;
        }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        ## Titulo ##
        header = QFrame()
        header.setStyleSheet("background:#E86A1E;border-radius:12px;")
        h_header = QHBoxLayout(header)
        h_header.setContentsMargins(16,10,16,10)

        bus = QLabel()
        bus.setFixedSize(72,72)
        pixmap = QPixmap(":/recursos/logocirculo.png").scaled(72,72,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        bus.setPixmap(pixmap)
        h_header.addWidget(bus)

        title = QLabel("Rutas Baja Express")
        title.setFont(QFont("Segoe UI",26,QFont.Bold))
        title.setStyleSheet("color:white;")
        title.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred)
        h_header.addWidget(title)

        map_img = QLabel()
        map_img.setFixedSize(72,72)
        pixmap_map = QPixmap(":/recursos/mapa de Baja Califor.png").scaled(92,92,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        map_img.setPixmap(pixmap_map)
        h_header.addWidget(map_img)

        root.addWidget(header)

        ## fondito azul ##
        blue = QFrame()
        blue.setStyleSheet("background:#0a79b7;border-radius:12px;")
        blue_l = QVBoxLayout(blue)
        blue_l.setContentsMargins(12,12,12,12)
        blue_l.setSpacing(14)

        ## buscador ##
        buscador = QFrame()
        buscador.setStyleSheet("background:white;border-radius:10px;")
        busc_l = QVBoxLayout(buscador)
        busc_l.setContentsMargins(30,12,30,12)
        busc_l.setSpacing(8)

        ## Filtros principales ##
        flow_container = QWidget()
        flow = FlowLayout(flow_container, margin=0, spacing=4)

        ## Función de placeholder ##
        def setupComboPlaceholder(combo, placeholder):
            combo.insertItem(0, placeholder)
            combo.setCurrentIndex(0)
            combo.view().setRowHidden(0, True)
            combo.setStyleSheet("QComboBox { color:#888; }")
            combo.currentIndexChanged.connect(
                lambda i: combo.setStyleSheet("QComboBox { color:black; }" if i!=0 else "QComboBox { color:#888; }")
            )

        ## ORIGEN ##
        self.cb_origin = QComboBox()
        self.cb_origin.setStyleSheet("QComboBox { color:black; }")

        # DESTINO #
        self.cb_dest = QComboBox()
        self.cb_dest.addItem("Todas")
        self.cb_dest.setStyleSheet("QComboBox { color:black; }")

        # FECHA #
        self.cb_date = QDateEdit()
        self.cb_date.setCalendarPopup(True)
        self.cb_date.setDate(QDate.currentDate())
        self.cb_date.setDisplayFormat("dd/MM/yyyy")

        # CHECKBOX FECHA EXACTA #
        checkbox_container = QWidget()
        checkbox_layout = QVBoxLayout(checkbox_container)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_layout.setAlignment(Qt.AlignCenter)
        
        self.checkbox_fecha_exacta = QCheckBox("Fecha exacta")
        self.checkbox_fecha_exacta.setToolTip("Activado: busca solo viajes en la fecha exacta\nDesactivado: busca viajes cercanos a la fecha")
        self.checkbox_fecha_exacta.setChecked(False)
        self.checkbox_fecha_exacta.setStyleSheet("""
            QCheckBox { 
                font-size: 13px; 
                padding: 8px;
                font-weight: 500;
            }
        """)
        checkbox_layout.addWidget(self.checkbox_fecha_exacta, alignment=Qt.AlignCenter)

        # Añadir widgets al flow #
        for w in (self.cb_origin, self.cb_dest, self.cb_date, checkbox_container):
            wrapper = QWidget()
            wrap_layout = QVBoxLayout(wrapper)
            wrap_layout.setContentsMargins(12,9,12,0)
            wrap_layout.addWidget(w)
            flow.addWidget(wrapper)

        # Segunda fila #
        bottom_row = QHBoxLayout()
        bottom_row.setContentsMargins(12, 0, 12, 0)
        bottom_row.addStretch()

        # Botón buscar #
        btn = QPushButton("➜")
        btn.setFixedSize(56,56)
        btn.setStyleSheet("background:#E86A1E;color:white;border-radius:12px;font-size:20px;")
        btn.clicked.connect(self.buscar_viajes)
        bottom_row.addWidget(btn)

        busc_l.addWidget(flow_container)
        busc_l.addLayout(bottom_row)

        blue_l.addWidget(buscador)

        ## Viajes disponibles ##
        lbl = QLabel("Viajes disponibles:")
        lbl.setFont(QFont("Segoe UI",20,QFont.Bold))
        lbl.setStyleSheet("color:white;")
        blue_l.addWidget(lbl)

        # Scroll viajes #
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameStyle(QFrame.NoFrame)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_widget)
        blue_l.addWidget(self.scroll_area,stretch=1)
        root.addWidget(blue,stretch=1)

        # Boton para regresar #
        back = QPushButton("Regresar")
        back.setFixedHeight(44)
        back.setStyleSheet("background:#E86A1E;color:white;border-radius:12px;")
        back.clicked.connect(self.close)
        root.addWidget(back,alignment=Qt.AlignLeft)

        # Cargar origenes y destinos #
        self.cargar_terminales()

        # Conectar búsqueda #
        btn.clicked.connect(self.buscar_viajes)

        # Mostrar todos los viajes futuros al inicio #
        self.cargar_viajes_futuros()

    # Consulta para terminales #
    def cargar_terminales(self):
        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM terminal ORDER BY nombre")
            nombres = [row[0] for row in cursor.fetchall()]
            
            # Cargar origen #
            self.cb_origin.addItems(nombres)
            
            # Dejar Tijuana como defecto #
            tijuana_index = self.cb_origin.findText("Tijuana", Qt.MatchFixedString)
            if tijuana_index >= 0:
                self.cb_origin.setCurrentIndex(tijuana_index)
            
            # Cargar destinos #
            self.cb_dest.addItems(nombres)
            
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self,"Error",f"No se pudieron cargar terminales:\n{e}")

    # Mostrar viajes #
    def cargar_viajes_futuros(self):
        for i in reversed(range(self.scroll_layout.count()-1)):
            item = self.scroll_layout.itemAt(i).widget()
            if item:
                item.setParent(None)

        try:
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)

            query = """
            SELECT v.numero AS viaje_num, v.fecHoraSalida, v.fecHoraEntrada, 
                   t_origen.nombre AS origen, t_destino.nombre AS destino,
                   r.duracion, r.precio, a.placas
            FROM viaje v
            JOIN ruta r ON v.ruta = r.codigo
            JOIN terminal t_origen ON r.origen = t_origen.numero
            JOIN terminal t_destino ON r.destino = t_destino.numero
            LEFT JOIN autobus a ON v.autobus = a.numero
            WHERE DATE(v.fecHoraSalida) >= CURDATE()
            ORDER BY v.fecHoraSalida ASC
            """
            cursor.execute(query)
            resultados = cursor.fetchall()

            if not resultados:
                QMessageBox.information(self, "Aviso", "No hay viajes programados")
                cursor.close()
                conn.close()
                return

            for viaje in resultados:
                self.scroll_layout.insertWidget(0, self._make_trip_card(viaje))

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los viajes:\n{e}")

    # Buscar viajes y aplicar filtros
    def buscar_viajes(self):
        origen = self.cb_origin.currentText() if self.cb_origin.currentText() else None
        destino_texto = self.cb_dest.currentText()
        destino = None if destino_texto == "Todas" else destino_texto
        fecha_seleccionada = self.cb_date.date().toPython()
        fecha_exacta = self.checkbox_fecha_exacta.isChecked()

        for i in reversed(range(self.scroll_layout.count()-1)):
            item = self.scroll_layout.itemAt(i).widget()
            if item:
                item.setParent(None)

        try:
            conn = crear_conexion()
            cursor = conn.cursor(dictionary=True)

            if fecha_exacta:
                query = """
                SELECT v.numero AS viaje_num, v.fecHoraSalida, v.fecHoraEntrada, 
                       t_origen.nombre AS origen, t_destino.nombre AS destino,
                       r.duracion, r.precio, a.placas
                FROM viaje v
                JOIN ruta r ON v.ruta = r.codigo
                JOIN terminal t_origen ON r.origen = t_origen.numero
                JOIN terminal t_destino ON r.destino = t_destino.numero
                LEFT JOIN autobus a ON v.autobus = a.numero
                WHERE (%s IS NULL OR t_origen.nombre = %s)
                  AND (%s IS NULL OR t_destino.nombre = %s)
                  AND DATE(v.fecHoraSalida) = %s
                ORDER BY v.fecHoraSalida
                """
                cursor.execute(query, (origen, origen, destino, destino, fecha_seleccionada))
            else:
                ## Búsqueda con fechas cercanas ##
                query = """
                SELECT v.numero AS viaje_num, v.fecHoraSalida, v.fecHoraEntrada, 
                       t_origen.nombre AS origen, t_destino.nombre AS destino,
                       r.duracion, r.precio, a.placas,
                       ABS(DATEDIFF(DATE(v.fecHoraSalida), %s)) AS dias_diferencia
                FROM viaje v
                JOIN ruta r ON v.ruta = r.codigo
                JOIN terminal t_origen ON r.origen = t_origen.numero
                JOIN terminal t_destino ON r.destino = t_destino.numero
                LEFT JOIN autobus a ON v.autobus = a.numero
                WHERE (%s IS NULL OR t_origen.nombre = %s)
                  AND (%s IS NULL OR t_destino.nombre = %s)
                  AND DATE(v.fecHoraSalida) >= CURDATE()
                  AND ABS(DATEDIFF(DATE(v.fecHoraSalida), %s)) <= 30
                ORDER BY dias_diferencia ASC, v.fecHoraSalida ASC
                LIMIT 20
                """
                cursor.execute(query, (
                    fecha_seleccionada,
                    origen, origen, 
                    destino, destino,
                    fecha_seleccionada
                ))

            resultados = cursor.fetchall()

            if not resultados:
                mensaje = "No hay viajes disponibles para la fecha exacta seleccionada." if fecha_exacta else "No hay viajes disponibles cerca de la fecha seleccionada (±30 días)."
                QMessageBox.information(self, "Aviso", mensaje)
                cursor.close()
                conn.close()
                return

            ## Mostrar mensaje si se encontraron viajes cercanos ##
            if not fecha_exacta and len(resultados) > 0:
                primer_viaje = resultados[0]
                fecha_encontrada = primer_viaje['fecHoraSalida'].date()
                if fecha_encontrada != fecha_seleccionada:
                    dias_diff = abs((fecha_encontrada - fecha_seleccionada).days)
                    info_label = QLabel(f"ℹ️ Mostrando viajes cercanos (más próximo: {dias_diff} día{'s' if dias_diff != 1 else ''} de diferencia)")
                    info_label.setStyleSheet("background:#ffffcc;color:#333;padding:8px;border-radius:6px;font-size:12px;")
                    info_label.setWordWrap(True)
                    self.scroll_layout.insertWidget(0, info_label)

            for viaje in resultados:
                self.scroll_layout.insertWidget(0, self._make_trip_card(viaje))

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los viajes:\n{e}")

    ## Carta de viaje ##
    def _make_trip_card(self, viaje):
        card = QFrame()
        card.setStyleSheet("background:white;border-radius:10px;")
        layout = QHBoxLayout(card)
        layout.setContentsMargins(12,12,12,12)

        # Imagen #
        img = QLabel()
        img.setFixedSize(140,90)
        pixmap = QPixmap(":/recursos/camiona.png").scaled(140,90,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        img.setPixmap(pixmap)
        layout.addWidget(img)

        # Info #
        center = QVBoxLayout()
        
        # Fecha del viaje en la parte superior #
        fecha_viaje_top = QLabel(viaje['fecHoraSalida'].strftime("%d/%m/%Y"))
        fecha_viaje_top.setStyleSheet("color:#0a79b7;font-weight:bold;font-size:12px;")
        fecha_viaje_top.setAlignment(Qt.AlignCenter)
        center.addWidget(fecha_viaje_top)
        
        top = QHBoxLayout()
        h1 = QLabel(viaje['fecHoraSalida'].strftime("%H:%M"))
        h1.setFont(QFont("Segoe UI",28,QFont.Bold))
        h2 = QLabel(viaje['fecHoraEntrada'].strftime("%H:%M"))
        h2.setFont(QFont("Segoe UI",28,QFont.Bold))
        top.addWidget(h1)
        top.addWidget(QLabel("●───────────────────────●"))
        top.addWidget(h2)
        center.addLayout(top)

        # Calcular duración real del viaje #
        duracion_calculada = viaje['fecHoraEntrada'] - viaje['fecHoraSalida']
        horas = duracion_calculada.total_seconds() // 3600
        minutos = (duracion_calculada.total_seconds() % 3600) // 60
        
        if horas > 0:
            duracion_texto = f"{int(horas)}h {int(minutos)}m"
        else:
            duracion_texto = f"{int(minutos)}m"

        bottom = QHBoxLayout()
        bottom.addWidget(QLabel(viaje['origen']))
        bottom.addStretch()
        
        # Duración calculada del viaje #
        duracion_label = QLabel(duracion_texto)
        duracion_label.setStyleSheet("color:#E86A1E;font-weight:bold;font-size:13px;")
        bottom.addWidget(duracion_label)
        bottom.addStretch()
        
        bottom.addWidget(QLabel(viaje['destino']))
        center.addLayout(bottom)
        layout.addLayout(center,stretch=1)

        # Precio y botón #
        price_l = QVBoxLayout()
        total = viaje['precio']
        price = QLabel(f"${total:.2f} MXN")
        price.setFont(QFont("Segoe UI",16,QFont.Bold))
        price.setStyleSheet("color:#E86A1E;")
        price_l.addWidget(price)

        btn_go = QPushButton("➜")
        btn_go.setFixedSize(56,56)
        btn_go.setStyleSheet("background:#E86A1E;color:white;border-radius:28px;")
        btn_go.clicked.connect(lambda _, id_v=viaje['viaje_num']: self.abrir_asientos(id_v, 1))
        price_l.addWidget(btn_go)
        layout.addLayout(price_l)

        return card

    # Asientos ##
    def abrir_asientos(self, id_viaje, num_pasajeros=1):
        self.ventana_asiento = VentanaAsientos(id_viaje, num_pasajeros)
        
        self.ventana_asiento.asientos_seleccionados.connect(
            lambda asientos: QMessageBox.information(
                self, "Asientos seleccionados",
                f"Seleccionaste los asientos: {asientos} para {num_pasajeros} pasajeros."
            )
        )
        
        # Mostrar ventana #
        self.ventana_asiento.show()

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()