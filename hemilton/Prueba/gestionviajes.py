"""
gestionviajes.py
Gestor de viajes - interfaz PySide6 (ESTILO MODERNO - CARDS VERTICALES)
Conexión real a MySQL usando conexion.crear_conexion()
"""

import sys
from datetime import datetime
from typing import List, Dict, Optional

from conexion import crear_conexion

from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QComboBox,
    QDateEdit, QHBoxLayout, QVBoxLayout, QPushButton, QDialog,
    QMessageBox, QFileDialog, QScrollArea, QFrame,
    QGroupBox, QTableWidget, QTableWidgetItem, QCalendarWidget, QSizePolicy
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QPixmap, QFont

# Importar recursos qrc compilados (asegúrate de que recursos_rc.py existe)
import recursos_rc


# ------------------------ UTIL ------------------------

def format_dt(dt: Optional[datetime]) -> str:
    if dt is None:
        return ""
    if isinstance(dt, str):
        return dt
    return dt.strftime("%Y-%m-%d %H:%M")


# ------------------------ DIALOGOS ------------------------

class BusDetailDialog(QDialog):
    """Muestra únicamente la información del autobús (sin pasajeros).
    Ahora adicionalmente consulta la cantidad de asientos por tipo desde la BD
    si se pasa una conexión (db_conn).
    """

    def __init__(self, trip: Dict, db_conn=None, parent=None):
        super().__init__(parent)
        self.trip = trip
        self.db_conn = db_conn
        self.setWindowTitle(f"Autobús asignado - Viaje {trip.get('trip_id')}")
        self.resize(600, 400)

        # STYLE
        self.setStyleSheet("""
            QWidget { background: #f8fafc; }
            QFrame#bus_container { background:white; border-radius:12px; padding:14px; border:1px solid #d9dfe5; }
            QLabel#title { font-size:20px; font-weight:700; color:#0b3a66; }
            QLabel#labelName { font-size:14px; color:#324a5e; }
            QLabel#labelValue { font-size:14px; font-weight:600; color:#1b2b3a; }
            QPushButton#closeBtn { background:#ff7b00; color:white; padding:8px 18px; border-radius:8px; }
            QPushButton#closeBtn:hover { background:#ff9c33; }
        """)

        main = QVBoxLayout(self)
        main.setContentsMargins(14, 14, 14, 14)

        title = QLabel(f"Información del Autobús – Viaje {trip.get('trip_id')}")
        title.setObjectName("title")
        title.setStyleSheet("font-size:18px; font-weight:700; color:#0b3a66;")
        main.addWidget(title)

        # Contenedor
        frame = QFrame()
        frame.setObjectName("bus_container")
        lay = QVBoxLayout(frame)
        lay.setSpacing(10)

        add_row = lambda name, value: self._add_row_to_layout(lay, name, value)

        add_row("Número del autobús:", trip.get("bus_number", ""))
        add_row("Matrícula:", trip.get("plate", ""))
        add_row("Marca:", trip.get("brand", ""))
        add_row("Modelo:", trip.get("model", ""))
        add_row("Año:", trip.get("year", ""))   # ← año desde BD
        add_row("Cantidad de asientos:", trip.get("seats_count", ""))

        # Si hay conexión a BD, consultamos asientos por tipo y mostramos
        if self.db_conn is not None:
            try:
                cur = self.db_conn.cursor(dictionary=True)
                # Consulta: cuenta de asientos por tipo con la descripción del tipo
                cur.execute("""
                    SELECT
                        COALESCE(ta.descripcion, a.tipo) AS tipo_desc,
                        a.tipo AS tipo_code,
                        COUNT(*) AS cnt
                    FROM asiento a
                    INNER JOIN tipo_asiento ta ON a.tipo = ta.codigo
                    WHERE a.autobus = %s
                    GROUP BY a.tipo
                    ORDER BY cnt DESC
                """, (trip.get("bus_number"),))
                rows = cur.fetchall()
                cur.close()

                if rows:
                    lines = []
                    total = 0
                    for r in rows:
                        tipo_desc = r.get("tipo_desc") or r.get("tipo_code") or ""
                        tipo_code = r.get("tipo_code") or ""
                        cnt = int(r.get("cnt") or 0)
                        total += cnt
                        lines.append(f"• {tipo_desc} ({tipo_code}): {cnt}")
                    # Si la suma difiere de seats_count, mantenemos ambos (informativo)
                    types_text = "\n".join(lines)
                    add_row("Asientos por tipo:", types_text)
                    # Mostrar total calculado (opcional, informativo)
                    if trip.get("seats_count") and int(trip.get("seats_count") or 0) != total:
                        add_row("Total (asientos tabla):", str(total))
                else:
                    add_row("Asientos por tipo:", "No se encontraron registros de asientos para este autobús.")
            except Exception as e:
                # No queremos romper el diálogo si falla la consulta; mostramos la excepción de forma limpia.
                add_row("Asientos por tipo:", f"Error al consultar BD: {e}")
        else:
            # Sin conexión BD, se puede mostrar un texto indicando que se requiere conexión para más detalle
            add_row("Asientos por tipo:", "Conexión BD no disponible — no se pueden obtener tipos de asiento.")

        main.addWidget(frame)

        btn = QPushButton("Cerrar")
        btn.setObjectName("closeBtn")
        btn.clicked.connect(self.close)
        main.addWidget(btn, alignment=Qt.AlignRight)

    def _add_row_to_layout(self, layout, name, value):
        row = QHBoxLayout()
        lbl = QLabel(name)
        lbl.setObjectName("labelName")
        val = QLabel(str(value) if value is not None else "")
        val.setObjectName("labelValue")
        val.setWordWrap(True)  # permitir saltos de línea para descripciones más largas
        lbl.setFixedWidth(180)
        row.addWidget(lbl)
        row.addWidget(val)
        row.addStretch()
        layout.addLayout(row)


class PassengersDialog(QDialog):
    """Muestra únicamente la lista de pasajeros para un viaje (consulta real)."""

    def __init__(self, trip: Dict, db_conn, parent=None):
        super().__init__(parent)
        self.trip = trip
        self.db_conn = db_conn

        self.setWindowTitle(f"Pasajeros del viaje {trip.get('trip_id')}")
        self.resize(720, 480)

        self.setStyleSheet("""
            QWidget { background:#f8fafc; }
            QLabel#title { font-size:20px; font-weight:700; color:#0b3a66; }
            QTableWidget { background:white; border-radius:8px; }
            QPushButton#closeBtn { background:#ff7b00; color:white; padding:8px 16px; border-radius:8px; }
            QPushButton#closeBtn:hover { background:#ff9c33; }
        """)

        main = QVBoxLayout(self)
        main.setContentsMargins(12, 12, 12, 12)

        title = QLabel(f"Pasajeros del Viaje {trip.get('trip_id')}")
        title.setObjectName("title")
        main.addWidget(title)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["# Ticket", "Nombre", "Edad", "Asiento", "Precio"])
        self.table.horizontalHeader().setStretchLastSection(True)
        # Ajuste de columnas
        self.table.setColumnWidth(0, 90)    # Ticket
        self.table.setColumnWidth(1, 250)   # Nombre completo (más grande)
        self.table.setColumnWidth(2, 60)    # Edad
        self.table.setColumnWidth(3, 70)    # Asiento
        self.table.setColumnWidth(4, 90)    # Precio (más pequeño)

        main.addWidget(self.table)

        # Botones
        btn_export = QPushButton("Exportar CSV")
        btn_export.clicked.connect(self.export_csv)

        btn_close = QPushButton("Cerrar")
        btn_close.setObjectName("closeBtn")
        btn_close.clicked.connect(self.close)

        h = QHBoxLayout()
        h.addStretch()
        h.addWidget(btn_export)
        h.addWidget(btn_close)
        main.addLayout(h)

        # Carga de datos
        try:
            self.load_passengers()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar pasajeros:\n{e}")

    def load_passengers(self):
        trip_id = self.trip.get("trip_id")
        cur = self.db_conn.cursor(dictionary=True)

        # --- CONSULTA NUEVA: nombre completo en un solo campo ---
        cur.execute("""
            SELECT
                t.codigo AS ticket_no,
                CONCAT(p.paNombre, ' ', p.paPrimerApell, ' ', COALESCE(p.paSegundoApell, '')) AS nombre_completo,
                p.edad AS edad,
                t.asiento AS asiento,
                t.precio AS precio
            FROM ticket t
            INNER JOIN pasajero p ON t.pasajero = p.num
            WHERE t.viaje = %s
            ORDER BY t.asiento ASC, p.paNombre ASC
        """, (trip_id,))

        rows = cur.fetchall()
        cur.close()

        self.table.setRowCount(len(rows))

        # --- YA SOLO 5 COLUMNAS (sin apellidos) ---
        for r, p in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(str(p.get("ticket_no", ""))))
            self.table.setItem(r, 1, QTableWidgetItem(str(p.get("nombre_completo", ""))))   # <- NOMBRE COMPLETO
            self.table.setItem(r, 2, QTableWidgetItem(str(p.get("edad", ""))))
            self.table.setItem(r, 3, QTableWidgetItem(str(p.get("asiento", ""))))
            self.table.setItem(r, 4, QTableWidgetItem(str(p.get("precio", ""))))

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar CSV", f"pasajeros_viaje_{self.trip.get('trip_id')}.csv", "CSV Files (*.csv)")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("ticket,nombre,apellidos,edad,asiento,precio\n")
                for r in range(self.table.rowCount()):
                    vals = [
                        self.table.item(r, c).text() if self.table.item(r, c) else ""
                        for c in range(self.table.columnCount())
                    ]
                    f.write(",".join(vals) + "\n")
            QMessageBox.information(self, "Listo", "CSV exportado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# ------------------------ WIDGET CARD ------------------------

class TripCard(QFrame):
    """
    Card vertical que muestra información del viaje y botones de acción.
    """
    def __init__(self, trip: Dict, parent=None):
        super().__init__(parent)
        self.trip = trip
        self.setObjectName("tripCard")
        self.setStyleSheet("""
            QFrame#tripCard { background: white; border-radius: 12px; border: 1px solid #d6dfe7; padding: 12px; }
            QLabel.title { font-size: 16px; font-weight: 700; color: #0b3a66; }
            QLabel.sub { font-size: 13px; color: #2f3f4f; }
            QLabel.meta { font-size: 12px; color: #5a6b78; }
            QPushButton.card-btn { background: #ff7b00; color: white; padding: 8px 14px; border-radius: 10px; font-weight: bold; }
            QPushButton.card-btn:hover { background: #ff9d3c; }
        """)

        left = QVBoxLayout()
        left.setSpacing(6)

        title = QLabel(f"Viaje #{trip['trip_id']} — Ruta #{trip['route_id']}")
        title.setProperty("class", "title")

        times = QLabel(f"Salida: {format_dt(trip.get('departure'))}   •   Llegada: {format_dt(trip.get('arrival'))}")
        times.setProperty("class", "sub")

        origin_city = trip.get("origin_city", "")
        origin_terminal = trip.get("origin_terminal", "")
        dest_city = trip.get("dest_city", "")
        dest_terminal = trip.get("dest_terminal", "")
        route = QLabel(f"{origin_city} {origin_terminal}  →  {dest_city} {dest_terminal}")
        route.setProperty("class", "sub")

        operator = QLabel(f"Operador: {trip.get('operator', '')}")
        operator.setProperty("class", "meta")

        bus = QLabel(f"Autobús: {trip.get('bus_number', '')}  •  Placas: {trip.get('plate', '')}")
        bus.setProperty("class", "meta")

        passengers = QLabel(f"Pasajeros vendidos: {trip.get('passengers_count', 0)}")
        passengers.setProperty("class", "meta")

        left.addWidget(title)
        left.addWidget(times)
        left.addWidget(route)
        left.addWidget(operator)
        left.addWidget(bus)
        left.addWidget(passengers)
        left.addStretch()

        right = QVBoxLayout()
        right.setSpacing(8)
        right.setAlignment(Qt.AlignTop | Qt.AlignRight)

        btn_detail = QPushButton("Autobús")
        btn_detail.setProperty("class", "card-btn")
        btn_detail.setFixedWidth(120)

        btn_pass = QPushButton("Pasajeros")
        btn_pass.setProperty("class", "card-btn")
        btn_pass.setFixedWidth(120)

        self.btn_detail = btn_detail
        self.btn_pass = btn_pass

        right.addWidget(btn_detail)
        right.addWidget(btn_pass)
        right.addStretch()

        main = QHBoxLayout()
        main.addLayout(left, 3)
        main.addLayout(right, 1)
        self.setLayout(main)


# ------------------------ VENTANA PRINCIPAL ------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Viajes - Rutas Baja Express")
        self.resize(1200, 750)

        try:
            self.db = crear_conexion()
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"No se pudo conectar a la BD:\n{e}")
            raise

        try:
            self.all_trips = self.load_trips_from_db()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los viajes:\n{e}")
            self.all_trips = []

        # ---------- HEADER (reemplazado por diseño solicitado) ----------
        header = QFrame()
        header.setStyleSheet("background:#E86A1E;border-radius:12px;")
        h_header = QHBoxLayout(header)
        h_header.setContentsMargins(16, 10, 16, 10)

        # Logo bus (usa recursos compilados)
        bus = QLabel()
        bus.setFixedSize(72, 72)
        try:
            pixmap = QPixmap(":/recursos/logocirculo.png")
            pixmap = pixmap.scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            bus.setPixmap(pixmap)
        except Exception:
            # si por alguna razón no carga, dejamos el QLabel vacío
            pass
        h_header.addWidget(bus)

        # Título grande centrado
        title = QLabel("Rutas Baja Express")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setStyleSheet("color:white;")
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        h_header.addWidget(title)

        # Imagen mapa a la derecha
        map_img = QLabel()
        map_img.setFixedSize(72, 72)
        try:
            pixmap_map = QPixmap(":/recursos/mapa de Baja Califor.png")
            pixmap_map = pixmap_map.scaled(92, 92, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            map_img.setPixmap(pixmap_map)
        except Exception:
            pass
        h_header.addWidget(map_img)
        # ----------------------------------------------------------------

        # ORIGEN: mostrar solo Tijuana (deshabilitado)
        lbl_o = QLabel("Origen:")
        self.cmb_origin = QComboBox()
        self.cmb_origin.addItem("Tijuana")
        self.cmb_origin.setCurrentIndex(0)
        self.cmb_origin.setEnabled(False)

        # DESTINO: versión mixta PERO SIN TIJUANA
        lbl_d = QLabel("Destino:")
        self.cmb_dest = QComboBox()
        self.cmb_dest.addItem("-- Todas --")

        forced_destinations = [
            "Mexicali",
            "Ensenada",
            "Tecate",
            "Rosarito",
            "San Quintin",
            "San Felipe"
        ]

        # Start with forced list
        items = [d for d in forced_destinations]
        seen = {d.lower() for d in items}

        # Add distinct DB destinations, EXCEPT Tijuana
        for t in self.all_trips:
            city = t.get("dest_city") or ""
            city = city.strip().title()
            if city and city.lower() != "tijuana" and city.lower() not in seen:
                seen.add(city.lower())
                items.append(city)

        self.cmb_dest.addItems(items)

        lbl_f = QLabel("Fecha:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setFixedWidth(150)
        self.date_edit.setDate(QDate.currentDate())

        # <<< ADICIÓN CALENDARIO BLANCO >>>
        # Creamos un QCalendarWidget personalizado y lo asignamos al QDateEdit
        cal = QCalendarWidget()
        cal.setStyleSheet("""
            QCalendarWidget {
                background-color: #ffffff;
                color: #0b3a66;
            }
            QCalendarWidget QWidget {
                background-color: #ffffff;
                color: #0b3a66;
            }
            QCalendarWidget QAbstractItemView {
                background-color: #ffffff;
                color: #0b3a66;
                selection-background-color: #4a90e2;
                selection-color: white;
            }
            QCalendarWidget QToolButton {
                background-color: #ffffff;
                color: #0b3a66;
            }
        """)
        # Asignamos el calendario al QDateEdit para asegurar el estilo del popup
        self.date_edit.setCalendarWidget(cal)
        # <<< FIN ADICIÓN CALENDARIO BLANCO >>>

        btn_filter = QPushButton("Filtrar")
        btn_filter.clicked.connect(self.apply_filters)
        

        btn_reset = QPushButton("Borrar")
        btn_reset.clicked.connect(self.reset_filters)

        # Estilo azul para ambos botones
        btn_filter.setStyleSheet("""
            QPushButton {
                background-color: #EF6C33;
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d85f2c;
            }
        """)

        btn_reset.setStyleSheet("""
            QPushButton {
                background-color: #EF6C33;
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d85f2c;
            }
        """)
        

        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(12)
        filter_layout.addWidget(lbl_o)
        filter_layout.addWidget(self.cmb_origin)
        filter_layout.addWidget(lbl_d)
        filter_layout.addWidget(self.cmb_dest)
        filter_layout.addWidget(lbl_f)
        filter_layout.addWidget(self.date_edit)
        filter_layout.addWidget(btn_filter)
        filter_layout.addWidget(btn_reset)
        filter_layout.addStretch()

        filters_frame = QFrame()
        f_layout = QHBoxLayout()
        f_layout.addLayout(filter_layout)
        filters_frame.setLayout(f_layout)
        filters_frame.setStyleSheet("background: transparent; padding: 8px;")

        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setSpacing(12)
        self.cards_layout.setContentsMargins(6, 6, 6, 6)
        self.cards_container.setLayout(self.cards_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.cards_container)

        central = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(header)             # <-- header con nuevo diseño
        main_layout.addSpacing(8)
        main_layout.addWidget(filters_frame)
        main_layout.addSpacing(6)
        main_layout.addWidget(self.scroll)
        central.setLayout(main_layout)
        self.setCentralWidget(central)

        self.apply_style()

        self.load_cards(self.all_trips)

    def apply_style(self):
         self.setStyleSheet("""
        QMainWindow { 
            background: #eef4fb; 
        }

        QLabel { 
            color: #0b3a66; 
            font-weight: 600; 
        }

        /* ---- CAMPOS ---- */
        QComboBox, QDateEdit {
            padding: 6px 10px;
            border-radius: 8px;
            border: 1px solid #cbd7e6;
            background: #ffffff;
            color: #0b3a66;
        }
        QComboBox:hover, QDateEdit:hover {
            border: 1px solid #4a90e2;
        }
        
        QComboBox:disabled {
            background: #f0f0f0;
            color: #888888;
            border: 1px solid #cbd7e6;
        }

        /* ---- POPUP DE COMBOBOX (totalmente blanco) ---- */
        QComboBox QAbstractItemView {
            background-color: #ffffff !important;
            color: #0b3a66 !important;
            border: 1px solid #cbd7e6 !important;
            padding: 4px;
            outline: none;
            selection-background-color: #4a90e2 !important;
            selection-color: white !important;
            min-width: 180px;
        }

        QComboBox QAbstractItemView::item {
            background-color: #ffffff !important;
            color: #0b3a66 !important;
            padding: 8px;
            border: none;
        }

        QComboBox QAbstractItemView::item:hover {
            background-color: #e3f2fd !important;
            color: #0b3a66 !important;
        }

        QComboBox QAbstractItemView::item:selected {
            background-color: #4a90e2 !important;
            color: white !important;
        }

        /* Scrollbar del ComboBox */
        QComboBox QAbstractItemView QScrollBar:vertical {
            background: #ffffff;
            width: 10px;
            border: none;
        }
        
        QComboBox QAbstractItemView QScrollBar::handle:vertical {
            background: #cbd7e6;
            border-radius: 5px;
            min-height: 20px;
        }
        
        QComboBox QAbstractItemView QScrollBar::handle:vertical:hover {
            background: #4a90e2;
        }

        /* ---- CALENDARIO DE QDateEdit (FORZAR TODO BLANCO) ---- */
        QCalendarWidget * {
            background-color: #ffffff !important;
            color: #0b3a66 !important;
        }
        
        QCalendarWidget {
            background-color: #ffffff !important;
            border: 1px solid #cbd7e6 !important;
            border-radius: 8px;
        }

        QCalendarWidget QWidget {
            background-color: #ffffff !important;
            color: #0b3a66 !important;
        }
        
        QCalendarWidget QTableView {
            background-color: #ffffff !important;
            color: #0b3a66 !important;
            gridline-color: #e0e0e0 !important;
            selection-background-color: #4a90e2 !important;
            selection-color: white !important;
            border: none !important;
        }

        /* Encabezado del calendario (días de la semana) */
        QCalendarWidget QWidget#qt_calendar_navigationbar {
            background-color: #ffffff !important;
            color: #0b3a66 !important;
        }

        /* números de los días */
        QCalendarWidget QAbstractItemView {
            background-color: #ffffff !important;
            color: #0b3a66 !important;
            selection-background-color: #4a90e2 !important;
            selection-color: white !important;
            border: none !important;
        }
        
        QCalendarWidget QAbstractItemView:enabled {
            background-color: #ffffff !important;
            color: #0b3a66 !important;
        }
        
        QCalendarWidget QAbstractItemView:disabled {
            background-color: #ffffff !important;
            color: #cccccc !important;
        }

        /* botones del calendario */
        QCalendarWidget QToolButton {
            background-color: #ffffff !important;
            color: #0b3a66 !important;
            font-weight: bold;
            border: none;
            padding: 5px;
        }
        
        QCalendarWidget QToolButton:hover {
            background-color: #e3f2fd !important;
            color: #4a90e2 !important;
            border-radius: 4px;
        }

        /* Botones de navegación (prev/next month) */
        QCalendarWidget QToolButton#qt_calendar_prevmonth,
        QCalendarWidget QToolButton#qt_calendar_nextmonth {
            background-color: #ffffff !important;
            color: #0b3a66 !important;
        }

        /* encargados de cambiar mes / año */
        QCalendarWidget QSpinBox {
            background-color: #ffffff !important;
            border: 1px solid #cbd7e6 !important;
            color: #0b3a66 !important;
            border-radius: 6px;
            padding: 3px;
        }
        
        QCalendarWidget QMenu {
            background-color: #ffffff !important;
            color: #0b3a66 !important;
            border: 1px solid #cbd7e6 !important;
        }
        
        /* Headers del mes/año */
        QCalendarWidget QAbstractButton {
            background-color: #ffffff !important;
            color: #0b3a66 !important;
        }

        QPushButton {
            background: #4a90e2;
            color: white;
            border-radius: 8px;
            padding: 6px 12px;
            font-weight: bold;
        }
        QPushButton:hover { background: #6ab0ff; }
    """)

    def clear_cards(self):
        for i in reversed(range(self.cards_layout.count())):
            w = self.cards_layout.itemAt(i).widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

    def load_cards(self, trips: List[Dict]):
        self.clear_cards()
        if not trips:
            lbl = QLabel("No se encontraron viajes con esos filtros.")
            lbl.setStyleSheet("color: #5a6b78; font-size: 14px;")
            self.cards_layout.addWidget(lbl)
            self.cards_layout.addStretch()
            return

        for trip in trips:
            card = TripCard(trip, parent=self)
            # ahora pasamos la conexión BD al diálogo de detalle
            card.btn_detail.clicked.connect(lambda _, t=trip: self.show_bus_detail(t))
            card.btn_pass.clicked.connect(lambda _, t=trip: self.show_passengers(t))
            self.cards_layout.addWidget(card)

        self.cards_layout.addStretch()

    def show_bus_detail(self, trip: Dict):
        # pasamos self.db para que el diálogo pueda consultar asientos por tipo
        dlg = BusDetailDialog(trip, self.db, parent=self)
        dlg.exec()

    def show_passengers(self, trip: Dict):
        try:
            dlg = PassengersDialog(trip, self.db, parent=self)
            dlg.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron abrir pasajeros:\n{e}")

    def apply_filters(self):
        origin = self.cmb_origin.currentText()
        dest = self.cmb_dest.currentText()

        qdate = self.date_edit.date().toPython() if hasattr(self.date_edit.date(), "toPython") else self.date_edit.date().toPyDate()

        results = []
        for t in self.all_trips:

            # Origen fijo Tijuana
            if t.get("origin_city") and t.get("origin_city").strip().lower() != "tijuana":
                continue

            # Filtro destino (sin Tijuana)
            if dest != "-- Todas --":
                if t.get("dest_city") and t.get("dest_city").strip().lower() != dest.strip().lower():
                    continue

            dep = t.get("departure")
            dep_date = dep.date() if isinstance(dep, datetime) else None
            if dep_date != qdate:
                continue

            results.append(t)

        self.load_cards(results)

    def reset_filters(self):
        self.cmb_dest.setCurrentIndex(0)
        self.date_edit.setDate(QDate.currentDate())
        self.load_cards(self.all_trips)

    # ---------------- DB ----------------

    def load_trips_from_db(self) -> List[Dict]:
        cur = self.db.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT
                    v.numero AS trip_id,
                    v.ruta AS route_id,
                    v.fecHoraSalida AS departure,
                    v.fecHoraEntrada AS arrival,
                    r.origen AS origin_terminal_num,
                    tor.nombre AS origin_terminal,
                    corig.nombre AS origin_city,
                    r.destino AS dest_terminal_num,
                    tdest.nombre AS dest_terminal,
                    cdest.nombre AS dest_city,
                    v.autobus AS bus_number,
                    a.placas AS plate,
                    mo.nombre AS model,
                    ma.nombre AS brand,
                    mo.numasientos AS seats_count,
                    mo.`año` AS year,
                    CONCAT(c.conNombre, ' ', c.conPrimerApell, ' ', COALESCE(c.conSegundoApell, '')) AS operator,
                    (SELECT COUNT(*) FROM ticket t WHERE t.viaje = v.numero) AS passengers_count,
                    v.estado AS estado
                FROM viaje v
                LEFT JOIN ruta r ON v.ruta = r.codigo
                LEFT JOIN terminal tor ON r.origen = tor.numero
                LEFT JOIN terminal tdest ON r.destino = tdest.numero
                LEFT JOIN ciudad corig ON tor.ciudad = corig.clave
                LEFT JOIN ciudad cdest ON tdest.ciudad = cdest.clave
                LEFT JOIN conductor c ON v.conductor = c.registro
                LEFT JOIN autobus a ON v.autobus = a.numero
                LEFT JOIN modelo mo ON a.modelo = mo.numero
                LEFT JOIN marca ma ON mo.marca = ma.numero
                ORDER BY v.fecHoraSalida ASC
            """)
            rows = cur.fetchall()

            trips = []
            for row in rows:
                trip = dict(row)
                trip['departure'] = row.get('departure')
                trip['arrival'] = row.get('arrival')
                trip['origin_city'] = (row.get('origin_city') or "").strip().title()
                trip['dest_city'] = (row.get('dest_city') or "").strip().title()
                trips.append(trip)

            return trips
        finally:
            cur.close()


# ------------------------ MAIN ------------------------

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()