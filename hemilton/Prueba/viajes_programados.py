# viajes_programados.py
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from conexion import crear_conexion
from PySide6.QtWidgets import QWidget, QApplication, QMessageBox, QDateTimeEdit, QDialogButtonBox
from PySide6.QtWidgets import (
    QLabel, QComboBox, QDateEdit, QHBoxLayout, QVBoxLayout, QPushButton,
    QScrollArea, QFrame, QSizePolicy, QDialog, QFormLayout, QGridLayout, QWidgetItem
)
from PySide6.QtCore import Qt, QDate, QDateTime, Signal, QObject
from PySide6.QtGui import QFont
from gestionviajes import PassengersDialog

# ------------------------ SIGNAL EMITTER ------------------------
class SignalEmitter(QObject):
    data_updated = Signal()

# ------------------------ UTIL ------------------------
def format_dt(dt: Optional[datetime]) -> str:
    if dt is None:
        return ""
    if isinstance(dt, str):
        return dt
    return dt.strftime("%Y-%m-%d %H:%M")

# ------------------------ TRIP CARD ------------------------
class TripCard(QFrame):
    def __init__(self, trip: Dict, parent=None):
        super().__init__(parent)
        self.trip = trip
        self.setObjectName("tripCard")

        self.setStyleSheet("""
            QFrame#tripCard {
                background: white;
                border-radius: 12px;
                border: 1px solid #d6dfe7;
                padding: 18px;
            }
            QLabel.title {
                font-size: 20px;
                font-weight: 900;
                color: #1A4A8D;
            }
            QLabel.label {
                font-size: 14px;
                font-weight: 600;
                color: #0b3a66;
            }
            QLabel.value {
                font-size: 14px;
                color: #425466;
            }
            QPushButton.card-btn {
                background: #EF6C33;
                color: white;
                padding: 6px 14px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton.card-btn:hover { background: #d85f2c; }
        """)

        # Layout principal simplificado
        left = QVBoxLayout()

        # 1) Salida (FECHA - HORA)
        salida_big = QLabel(f"Salida: {format_dt(trip.get('departure'))}")
        salida_big.setProperty("class", "title")
        left.addWidget(salida_big)
        left.addSpacing(4)

        # 2) Número de viaje
        viaje_lbl = QLabel(f"Viaje #{trip.get('trip_id')}")
        viaje_lbl.setProperty("class", "label")
        left.addWidget(viaje_lbl)
        left.addSpacing(6)

        # 3) Ciudad de origen → destino
        origen_destino = QLabel(f"{trip.get('origin_city','')} → {trip.get('dest_city','')}")
        origen_destino.setProperty("class", "value")
        left.addWidget(origen_destino)
        left.addSpacing(6)

        # 4) Autobús y conductor
        autobus_lbl = QLabel(f"Autobús: {trip.get('bus_number','')} | Conductor: {trip.get('operator','')}")
        autobus_lbl.setProperty("class", "value")
        left.addWidget(autobus_lbl)

        left.addStretch()

        # Botón DETALLES a la derecha
        btn_layout = QVBoxLayout()
        self.btn_details = QPushButton("Detalles")
        self.btn_details.setProperty("class", "card-btn")
        btn_layout.addWidget(self.btn_details, alignment=Qt.AlignRight)
        btn_layout.addStretch()

        main = QHBoxLayout(self)
        main.addLayout(left, 4)
        main.addLayout(btn_layout, 1)

# ------------------------ MAIN WINDOW ------------------------
class ProgramacionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Salidas - Rutas Baja Express")
        self.resize(1100, 700)

        self.all_trips: List[Dict] = []
        self.load_all_trips_from_db()

        # Crear el emisor de señales
        self.signal_emitter = SignalEmitter()

        # ---------- FILTERS ----------
        lbl_fecha = QLabel("Fecha:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumWidth(120)
        self.date_edit.setDate(QDate.currentDate())

        lbl_origen = QLabel("Origen:")
        self.cmb_origen = QComboBox()
        self.cmb_origen.setMinimumWidth(150)

        lbl_dest = QLabel("Destino:")
        self.cmb_dest = QComboBox()
        self.cmb_dest.setMinimumWidth(150)

        btn_apply = QPushButton("Filtrar")
        btn_apply.clicked.connect(self.apply_filters)

        btn_clear = QPushButton("Limpiar Filtros")
        btn_clear.setObjectName("clearBtn")
        btn_clear.clicked.connect(self.clear_filters)

        btn_add_trip = QPushButton("Agregar Salida")
        btn_add_trip.clicked.connect(self.open_add_trip_dialog)

        # ----- LAYOUT HORIZONTAL DE LOS FILTROS -----
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        filter_layout.setContentsMargins(0, 0, 0, 0)

        filter_layout.addWidget(lbl_fecha)
        filter_layout.addWidget(self.date_edit)
        filter_layout.addWidget(lbl_origen)
        filter_layout.addWidget(self.cmb_origen)
        filter_layout.addWidget(lbl_dest)
        filter_layout.addWidget(self.cmb_dest)

        # ----- CONTENEDOR DE LOS FILTROS -----
        filters_frame = QFrame()
        filters_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        f_layout = QHBoxLayout(filters_frame)
        f_layout.setContentsMargins(0, 0, 0, 0)
        f_layout.setSpacing(0)
        f_layout.addStretch(1)
        f_layout.addLayout(filter_layout)
        f_layout.addStretch(1)

        # ----- BOTONES DE ACCIÓN -----
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(btn_apply)
        buttons_layout.addWidget(btn_clear)
        buttons_layout.addWidget(btn_add_trip)
        buttons_layout.addStretch(1)

        # ---------- CARDS ----------
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout()
        self.cards_container.setLayout(self.cards_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.cards_container)

        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.addWidget(filters_frame)
        main_layout.addWidget(buttons_frame)
        main_layout.addWidget(self.scroll)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(central)
        
        self.apply_style()
        self.populate_filter_boxes()
        
        # Mostrar TODOS los viajes al iniciar (sin filtrar)
        self.load_cards(self.all_trips)

    def get_signal_emitter(self):
        """Devuelve el emisor de señales para conectarlo desde el PanelAdministrador"""
        return self.signal_emitter

    # ---------- ESTILOS GLOBALES ----------
    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow { background: #f3f7fb; }
            QLabel { color: #0b3a66; font-weight: 600; }

            QComboBox {
                padding: 6px 10px;
                border-radius: 8px;
                border: 1px solid #cbd7e6;
                background: #ffffff;
                color: #0b3a66;
            }
            QComboBox::down-arrow { image: none; }
            QComboBox::drop-down { width: 0px; border: none; }
            QComboBox QAbstractItemView {
                background: #ffffff;
                color: #0b3a66;
                selection-background-color: #EF6C33;
                selection-color: white;
                outline: 0;
            }

            QDateEdit {
                padding: 6px 10px;
                border-radius: 8px;
                border: 1px solid #cbd7e6;
                background: #ffffff;
                color: #0b3a66;
            }
            QDateEdit::down-arrow { image: none; width: 0px; }
            QDateEdit::drop-down { width: 20px; border: none; }

            QPushButton {
                background: #EF6C33;
                color: white;
                border-radius: 8px;
                padding: 6px 10px;
                font-weight: bold;
            }
            QPushButton:hover { background: #d85f2c; }
            
            QPushButton#clearBtn {
                background: #6c757d;
                color: white;
                border-radius: 8px;
                padding: 6px 10px;
                font-weight: bold;
            }
            QPushButton#clearBtn:hover { 
                background: #5a6268; 
            }
        """)

    # ---------- CARDS CONTROL ----------
    def clear_cards(self):
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def load_cards(self, trips: List[Dict]):
        self.clear_cards()

        if not trips:
            lbl = QLabel("No hay salidas programadas para los filtros seleccionados.")
            lbl.setStyleSheet("color: #5a6b78; font-size: 14px;")
            self.cards_layout.addWidget(lbl)
            self.cards_layout.addStretch()
            return

        for trip in trips:
            card = TripCard(trip, parent=self)
            card.btn_details.clicked.connect(lambda _, t=trip: self.show_trip_details(t))
            self.cards_layout.addWidget(card)

        self.cards_layout.addStretch()
        self.cards_container.updateGeometry()
        self.scroll.widget().adjustSize()
        self.scroll.updateGeometry()
        QApplication.processEvents()

    def show_trip_details(self, trip: Dict):
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Detalles del Viaje #{trip.get('trip_id')}")
        dlg.resize(700, 550)

        dlg.setStyleSheet("""
            QDialog { background: #f4f7fb; }
            QFrame#detailCard {
                background: white;
                border-radius: 14px;
                border: 1px solid #d6dfe7;
                padding: 22px;
            }
            QLabel.title {
                font-size: 24px;
                font-weight: 900;
                color: #1A4A8D;
                margin-bottom: 10px;
            }
            QLabel.subtitle {
                font-size: 14px;
                font-weight: 700;
                color: #0b3a66;
                margin-top: 8px;
            }
            QLabel.data {
                font-size: 13px;
                color: #415466;
                padding: 4px 0px;
            }
            QPushButton#closeBtn {
                background: #EF6C33;
                color: white;
                padding: 10px 30px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#closeBtn:hover { background: #d85f2c; }
        """)

        # Card container
        card = QFrame()
        card.setObjectName("detailCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)

        # Title
        title = QLabel(f"Viaje #{trip.get('trip_id')} — Ruta #{trip.get('route_id')}")
        title.setProperty("class", "title")
        card_layout.addWidget(title)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content_widget = QWidget()
        # We'll use a QVBoxLayout to stack block containers (each block can be a grid)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(12)

        # -------- BLOQUE 2: Fecha y hora de salida / Fecha y hora de llegada --------
        block2 = QFrame()
        b2_layout = QGridLayout(block2)
        b2_layout.setContentsMargins(0, 0, 0, 0)
        b2_layout.setHorizontalSpacing(20)
        b2_layout.setVerticalSpacing(6)

        lbl_salida_label = QLabel("Fecha y hora de salida")
        lbl_salida_label.setProperty("class", "subtitle")
        lbl_salida_value = QLabel(format_dt(trip.get("departure")))
        lbl_salida_value.setProperty("class", "data")

        lbl_llegada_label = QLabel("Fecha y hora de llegada")
        lbl_llegada_label.setProperty("class", "subtitle")
        lbl_llegada_value = QLabel(format_dt(trip.get("arrival")))
        lbl_llegada_value.setProperty("class", "data")

        b2_layout.addWidget(lbl_salida_label, 0, 0)
        b2_layout.addWidget(lbl_llegada_label, 0, 1)
        b2_layout.addWidget(lbl_salida_value, 1, 0)
        b2_layout.addWidget(lbl_llegada_value, 1, 1)

        content_layout.addWidget(block2)

        # -------- BLOQUE 3: Origen / Terminal de salida  AND Destino / Terminal de llegada --------
        block3 = QFrame()
        b3_layout = QGridLayout(block3)
        b3_layout.setContentsMargins(0, 0, 0, 0)
        b3_layout.setHorizontalSpacing(20)
        b3_layout.setVerticalSpacing(6)

        lbl_origen_ciudad_label = QLabel("Nombre de la ciudad de origen")
        lbl_origen_ciudad_label.setProperty("class", "subtitle")
        lbl_origen_ciudad_value = QLabel(trip.get("origin_city", "N/A"))
        lbl_origen_ciudad_value.setProperty("class", "data")

        lbl_origen_terminal_label = QLabel("Nombre de la terminal donde salen")
        lbl_origen_terminal_label.setProperty("class", "subtitle")
        lbl_origen_terminal_value = QLabel(trip.get("origin_terminal", "N/A"))
        lbl_origen_terminal_value.setProperty("class", "data")

        lbl_dest_ciudad_label = QLabel("Nombre de la ciudad de destino")
        lbl_dest_ciudad_label.setProperty("class", "subtitle")
        lbl_dest_ciudad_value = QLabel(trip.get("dest_city", "N/A"))
        lbl_dest_ciudad_value.setProperty("class", "data")

        lbl_dest_terminal_label = QLabel("Nombre de la terminal donde llegan")
        lbl_dest_terminal_label.setProperty("class", "subtitle")
        lbl_dest_terminal_value = QLabel(trip.get("dest_terminal", "N/A"))
        lbl_dest_terminal_value.setProperty("class", "data")

        # First row
        b3_layout.addWidget(lbl_origen_ciudad_label, 0, 0)
        b3_layout.addWidget(lbl_origen_terminal_label, 0, 1)
        # Second row: values for first row
        b3_layout.addWidget(lbl_origen_ciudad_value, 1, 0)
        b3_layout.addWidget(lbl_origen_terminal_value, 1, 1)
        # Third row: destination labels
        b3_layout.addWidget(lbl_dest_ciudad_label, 2, 0)
        b3_layout.addWidget(lbl_dest_terminal_label, 2, 1)
        # Fourth row: destination values
        b3_layout.addWidget(lbl_dest_ciudad_value, 3, 0)
        b3_layout.addWidget(lbl_dest_terminal_value, 3, 1)

        content_layout.addWidget(block3)

        # -------- BLOQUE 4: Nombre completo del operador (full width) --------
        block4 = QFrame()
        b4_layout = QVBoxLayout(block4)
        b4_layout.setContentsMargins(0, 0, 0, 0)
        b4_layout.setSpacing(6)

        lbl_operador_label = QLabel("Nombre completo del operador")
        lbl_operador_label.setProperty("class", "subtitle")
        lbl_operador_value = QLabel(trip.get("operator", "Sin asignar"))
        lbl_operador_value.setProperty("class", "data")

        b4_layout.addWidget(lbl_operador_label)
        b4_layout.addWidget(lbl_operador_value)

        content_layout.addWidget(block4)

        # -------- BLOQUE 5: Número de autobús / Matrícula  AND Cantidad asientos / Cantidad pasajeros --------
        block5 = QFrame()
        b5_layout = QGridLayout(block5)
        b5_layout.setContentsMargins(0, 0, 0, 0)
        b5_layout.setHorizontalSpacing(20)
        b5_layout.setVerticalSpacing(6)

        lbl_bus_num_label = QLabel("Número del autobús asignado")
        lbl_bus_num_label.setProperty("class", "subtitle")
        lbl_bus_num_value = QLabel(str(trip.get("bus_number", "N/A")))
        lbl_bus_num_value.setProperty("class", "data")

        lbl_plate_label = QLabel("Matrícula del autobús asignado")
        lbl_plate_label.setProperty("class", "subtitle")
        lbl_plate_value = QLabel(trip.get("plate", "N/A"))
        lbl_plate_value.setProperty("class", "data")

        lbl_seats_label = QLabel("Cantidad de asientos del autobús")
        lbl_seats_label.setProperty("class", "subtitle")
        lbl_seats_value = QLabel(str(trip.get("seats_count", 0)))
        lbl_seats_value.setProperty("class", "data")

        lbl_passengers_label = QLabel("Cantidad de pasajeros")
        lbl_passengers_label.setProperty("class", "subtitle")
        lbl_passengers_value = QLabel(str(trip.get("passengers_count", 0)))
        lbl_passengers_value.setProperty("class", "data")

        # First row: bus number and plate labels
        b5_layout.addWidget(lbl_bus_num_label, 0, 0)
        b5_layout.addWidget(lbl_plate_label, 0, 1)
        # Second row: bus number and plate values
        b5_layout.addWidget(lbl_bus_num_value, 1, 0)
        b5_layout.addWidget(lbl_plate_value, 1, 1)
        # Third row: seats and passengers labels
        b5_layout.addWidget(lbl_seats_label, 2, 0)
        b5_layout.addWidget(lbl_passengers_label, 2, 1)
        # Fourth row: seats and passengers values
        b5_layout.addWidget(lbl_seats_value, 3, 0)
        b5_layout.addWidget(lbl_passengers_value, 3, 1)

        content_layout.addWidget(block5)

        # stretch at end so content doesn't stick
        content_layout.addStretch()
        scroll.setWidget(content_widget)
        card_layout.addWidget(scroll)

        # Botón cerrar
        btn_close = QPushButton("Cerrar")
        btn_close.setObjectName("closeBtn")
        btn_close.clicked.connect(dlg.close)

        root = QVBoxLayout(dlg)
        root.addWidget(card)
        root.addWidget(btn_close, alignment=Qt.AlignCenter)
        dlg.exec()

    def load_all_trips_from_db(self):
        """Carga TODOS los viajes futuros (sin filtro de fecha pasada)"""
        try:
            cn = crear_conexion()
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"No se pudo conectar a la BD:\n{e}")
            return

        cur = cn.cursor(dictionary=True)

        try:
            # Agregamos WHERE v.fecHoraSalida >= NOW() para filtrar solo viajes futuros
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

        CONCAT(
            c.conNombre, ' ',
            c.conPrimerApell, ' ',
            IFNULL(c.conSegundoApell, '')
        ) AS operator,

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
    WHERE v.fecHoraSalida >= NOW()
    ORDER BY v.fecHoraSalida ASC
    """)

            rows = cur.fetchall()
            trips = []

            for row in rows:
                trip = dict(row)
                trip["origin_city"] = (row.get("origin_city") or "Sin ciudad").strip().title()
                trip["dest_city"] = (row.get("dest_city") or "Sin ciudad").strip().title()
                trips.append(trip)

            self.all_trips = trips

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar viajes: {e}")
        finally:
            cur.close()
            cn.close()
    # ---------- FILTROS ----------
    def populate_filter_boxes(self):
        origenes = set()
        destinos = set()

        for t in self.all_trips:
            origen = (t.get("origin_city") or "").strip().title()
            destino = (t.get("dest_city") or "").strip().title()
            if origen:
                origenes.add(origen)
            if destino:
                destinos.add(destino)

        sorted_origenes = sorted(origenes)
        sorted_destinos = sorted(destinos)

        current_origen = self.cmb_origen.currentText()
        current_dest = self.cmb_dest.currentText()

        self.cmb_origen.clear()
        self.cmb_origen.addItem("-- Todas --")
        self.cmb_origen.addItems(sorted_origenes)

        self.cmb_dest.clear()
        self.cmb_dest.addItem("-- Todas --")
        self.cmb_dest.addItems(sorted_destinos)

        if current_origen:
            idx_origen = self.cmb_origen.findText(current_origen)
            if idx_origen >= 0:
                self.cmb_origen.setCurrentIndex(idx_origen)
            else:
                idx_tijuana = self.cmb_origen.findText("Tijuana")
                if idx_tijuana >= 0:
                    self.cmb_origen.setCurrentIndex(idx_tijuana)
                else:
                    self.cmb_origen.setCurrentIndex(0)
        else:
            idx_tijuana = self.cmb_origen.findText("Tijuana")
            if idx_tijuana >= 0:
                self.cmb_origen.setCurrentIndex(idx_tijuana)
            else:
                self.cmb_origen.setCurrentIndex(0)

        idx_dest = self.cmb_dest.findText(current_dest)
        if idx_dest >= 0:
            self.cmb_dest.setCurrentIndex(idx_dest)
        else:
            self.cmb_dest.setCurrentIndex(0)

    def apply_filters(self):
        filtered = self.all_trips
        selected_date = self.date_edit.date().toPython()
        origen = self.cmb_origen.currentText().strip()
        dest = self.cmb_dest.currentText().strip()

        if selected_date != QDate.currentDate().toPython():
            filtered = [t for t in filtered if t["departure"].date() == selected_date]

        if origen and origen != "-- Todas --":
            filtered = [t for t in filtered if t["origin_city"].lower() == origen.lower()]

        if dest and dest != "-- Todas --":
            filtered = [t for t in filtered if t["dest_city"].lower() == dest.lower()]

        self.load_cards(filtered)

    def clear_filters(self):
        """Limpia todos los filtros y muestra todos los viajes"""
        # Restablecer fecha a hoy
        self.date_edit.setDate(QDate.currentDate())
        
        # Restablecer origen a "Tijuana" o "-- Todas --"
        idx_tijuana = self.cmb_origen.findText("Tijuana")
        if idx_tijuana >= 0:
            self.cmb_origen.setCurrentIndex(idx_tijuana)
        else:
            self.cmb_origen.setCurrentIndex(0)  # "-- Todas --"
        
        # Restablecer destino a "-- Todas --"
        self.cmb_dest.setCurrentIndex(0)
        
        # Mostrar TODOS los viajes
        self.load_cards(self.all_trips)

    # ---------- AGREGAR SALIDA ----------
    def open_add_trip_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Agregar Nueva Salida")
        dlg.setMinimumWidth(500)

        layout = QFormLayout(dlg)

        self.departure_edit = QDateTimeEdit()
        self.departure_edit.setDateTime(QDateTime.currentDateTime().addDays(1))
        self.departure_edit.setCalendarPopup(True)
        self.departure_edit.setDisplayFormat("yyyy-MM-dd HH:mm")

        self.arrival_edit = QDateTimeEdit()
        self.arrival_edit.setDateTime(QDateTime.currentDateTime().addDays(1).addSecs(3600))
        self.arrival_edit.setCalendarPopup(True)
        self.arrival_edit.setDisplayFormat("yyyy-MM-dd HH:mm")

        self.route_combo = QComboBox()
        self.bus_combo = QComboBox()
        self.driver_combo = QComboBox()
        self.status_combo = QComboBox()

        self.load_combo_data()

        layout.addRow("Fecha y Hora de Salida:", self.departure_edit)
        layout.addRow("Fecha y Hora de Llegada:", self.arrival_edit)
        layout.addRow("Ruta:", self.route_combo)
        layout.addRow("Autobús:", self.bus_combo)
        layout.addRow("Conductor:", self.driver_combo)
        layout.addRow("Estado:", self.status_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.add_trip(dlg))
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)

        dlg.exec()

    def load_combo_data(self):
        try:
            cn = crear_conexion()
            cur = cn.cursor(dictionary=True)

            cur.execute("""
                SELECT r.codigo, CONCAT(c1.nombre, ' → ', c2.nombre) AS ruta_desc
                FROM ruta r
                JOIN terminal t1 ON r.origen = t1.numero
                JOIN terminal t2 ON r.destino = t2.numero
                JOIN ciudad c1 ON t1.ciudad = c1.clave
                JOIN ciudad c2 ON t2.ciudad = c2.clave
                ORDER BY c1.nombre, c2.nombre
            """)
            for row in cur.fetchall():
                self.route_combo.addItem(f"Ruta #{row['codigo']} ({row['ruta_desc']})", row['codigo'])

            cur.execute("SELECT numero, placas FROM autobus ORDER BY numero")
            for row in cur.fetchall():
                self.bus_combo.addItem(f"Autobús #{row['numero']} ({row['placas']})", row['numero'])

            cur.execute("SELECT registro, CONCAT(conNombre, ' ', conPrimerApell) AS nombre FROM conductor ORDER BY conNombre")
            for row in cur.fetchall():
                self.driver_combo.addItem(f"{row['nombre']} (#{row['registro']})", row['registro'])

            cur.execute("SELECT numero, nombre FROM edo_viaje ORDER BY numero")
            for row in cur.fetchall():
                self.status_combo.addItem(row['nombre'], row['numero'])

            cur.close()
            cn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los datos: {e}")

    def add_trip(self, dialog):
        departure = self.departure_edit.dateTime().toPython()
        arrival = self.arrival_edit.dateTime().toPython()
        route = self.route_combo.currentData()
        bus = self.bus_combo.currentData()
        driver = self.driver_combo.currentData()
        status = self.status_combo.currentData()

        if not all([departure, arrival, route, bus, driver, status]):
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios")
            return

        if arrival <= departure:
            QMessageBox.warning(self, "Advertencia", "La hora de llegada debe ser posterior a la de salida")
            return

        try:
            cn = crear_conexion()
            cur = cn.cursor()

            cur.execute("""
                INSERT INTO viaje (fecHoraSalida, fecHoraEntrada, ruta, estado, autobus, conductor)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (departure, arrival, route, status, bus, driver))

            trip_id = cur.lastrowid

            cur.execute("SELECT numero FROM asiento WHERE autobus = %s", (bus,))
            seats = cur.fetchall()

            for seat in seats:
                seat_number = seat[0]
                cur.execute("""
                    INSERT INTO viaje_asiento (asiento, viaje, ocupado)
                    VALUES (%s, %s, %s)
                """, (seat_number, trip_id, False))

            cn.commit()
            cur.close()
            cn.close()

            QMessageBox.information(self, "Éxito", "Salida agregada correctamente.")
            dialog.accept()

            # RECARGAR Y MOSTRAR EL NUEVO VIAJE
            self.load_all_trips_from_db()
            self.populate_filter_boxes()
            self.load_cards(self.all_trips)  # Mostrar TODOS los viajes
            self.signal_emitter.data_updated.emit()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar la salida: {e}")

# ------------------------ MAIN ------------------------
def main():
    app = QApplication(sys.argv)
    win = ProgramacionWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()