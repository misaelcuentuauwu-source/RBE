# viajes_programados.py
# Interfaz PySide6 — "Viajes Programados"

import sys
from datetime import datetime
from typing import List, Dict, Optional

from conexion import crear_conexion
from PySide6.QtWidgets import QWidget

from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QComboBox,
    QDateEdit, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox,
    QScrollArea, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont


# ------------------------ UTIL ------------------------

def format_dt(dt: Optional[datetime]) -> str:
    if dt is None:
        return ""
    if isinstance(dt, str):
        return dt
    return dt.strftime("%Y-%m-%d %H:%M")


# ------------------------ TRIP CARD (CORREGIDA) ------------------------

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
                padding: 12px;
            }

            /* Estilos texto */
            QLabel.bigblue { 
                font-size: 22px; 
                font-weight: 900; 
                color: #1A4A8D; 
            }
            QLabel.title { 
                font-size: 15px; 
                font-weight: 700; 
                color: #0b3a66; 
            }
            QLabel.sub { 
                font-size: 14px; 
                color: #2f3f4f; 
            }
            QLabel.meta { 
                font-size: 12px; 
                color: #5a6b78; 
            }

            QPushButton.card-btn {
                background: #EF6C33;
                color: white;
                padding: 6px 12px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton.card-btn:hover { background: #d85f2c; }
        """)

        # -----------------------------------------------------------
        # ORDEN FINAL (solicitado)
        # 1. Salida (GRANDE y AZUL)
        # 2. Llegada
        # 3. Número de viaje (normal)
        # 4. Origen
        # 5. Destino
        # 6. Autobús
        # 7. Estado
        # -----------------------------------------------------------

        left = QVBoxLayout()
        left.setSpacing(4)

        # 🔵 GRANDE Y AZUL — TIPO PANTALLA DE AEROPUERTO
        salida = QLabel(f"Salida: {format_dt(trip.get('departure'))}")
        salida.setProperty("class", "bigblue")

        llegada = QLabel(f"Llegada: {format_dt(trip.get('arrival'))}")
        llegada.setProperty("class", "sub")

        viaje = QLabel(f"Viaje #{trip.get('trip_id', '')}")
        viaje.setProperty("class", "title")  # tamaño normal

        origen = QLabel(f"Origen: {trip.get('origin_city','')}")
        origen.setProperty("class", "sub")

        destino = QLabel(f"Destino: {trip.get('dest_city','')}")
        destino.setProperty("class", "sub")

        autobus = QLabel(f"Autobús: {trip.get('bus_number','')}")
        autobus.setProperty("class", "meta")

        estado = QLabel(f"Estado: {trip.get('estado_nombre','')}")
        estado.setProperty("class", "meta")

        # Agregar en orden
        left.addWidget(salida)
        left.addWidget(llegada)
        left.addWidget(viaje)
        left.addWidget(origen)
        left.addWidget(destino)
        left.addWidget(autobus)
        left.addWidget(estado)
        left.addStretch()

        # ------- Botón a la derecha -------
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignTop | Qt.AlignRight)

        btn_details = QPushButton("Detalles")
        btn_details.setProperty("class", "card-btn")
        btn_details.setFixedWidth(120)
        self.btn_details = btn_details

        right.addWidget(btn_details)
        right.addStretch()

        main = QHBoxLayout()
        main.addLayout(left, 3)
        main.addLayout(right, 1)
        self.setLayout(main)


# ------------------------ MAIN WINDOW ------------------------

class ProgramacionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Viajes Programados - Programación del Día")
        self.resize(1100, 700)

        try:
            self.db = crear_conexion()
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"No se pudo conectar a la BD:\n{e}")
            raise

        self.all_trips: List[Dict] = []
        self.load_all_trips_from_db()

        # ---------- FILTERS ----------
        lbl_fecha = QLabel("Fecha:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumWidth(120)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.userChanged = False
        self.date_edit.dateChanged.connect(lambda: setattr(self.date_edit, "userChanged", True))

        lbl_origen = QLabel("Origen:")
        self.cmb_origen = QComboBox()
        self.cmb_origen.setMinimumWidth(150)

        lbl_dest = QLabel("Destino:")
        self.cmb_dest = QComboBox()
        self.cmb_dest.setMinimumWidth(150)

        btn_apply = QPushButton("Filtrar")
        btn_apply.clicked.connect(self.apply_filters)

        btn_reset = QPushButton("Borrar")
        btn_reset.clicked.connect(self.reset_filters)

        btn_update = QPushButton("Actualizar")
        btn_update.clicked.connect(self.reload_from_db)

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





        # IMPORTANTE: NO PONER AQUI EL addStretch() porque causa colapso
        # filter_layout.addStretch()


        # ----- CONTENEDOR DE LOS FILTROS -----
        filters_frame = QFrame()
        filters_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        f_layout = QHBoxLayout(filters_frame)
        f_layout.setContentsMargins(0, 0, 0, 0)
        f_layout.setSpacing(0)

        # Esto evita que los widgets se apilen en vertical
        f_layout.addStretch(1)          # espacio a la izquierda
        f_layout.addLayout(filter_layout) 
        f_layout.addStretch(1)          # espacio a la derecha


        # ----- BOTONES DE ACCIÓN ABAJO -----
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)

        buttons_layout.addStretch(1)
        buttons_layout.addWidget(btn_apply)
        buttons_layout.addWidget(btn_reset)
        buttons_layout.addWidget(btn_update)
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

        # Reemplazo de setCentralWidget
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(central)
        self.apply_style()
        self.populate_filter_boxes()
        self.load_cards(self.all_trips)

    # ---------- ESTILOS GLOBALES ----------

    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow { background: #f3f7fb; }
            QLabel { color: #0b3a66; font-weight: 600; }

            /* COMBOBOX */
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

            /* QDateEdit */
            QDateEdit {
                padding: 6px 10px;
                border-radius: 8px;
                border: 1px solid #cbd7e6;
                background: #ffffff;
                color: #0b3a66;
            }
            QDateEdit::down-arrow { image: none; width: 0px; }
            QDateEdit::drop-down { width: 20px; border: none; }

            /* BOTONES */
            QPushButton {
                background: #EF6C33;
                color: white;
                border-radius: 8px;
                padding: 6px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #d85f2c;
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
            lbl = QLabel("No hay viajes programados para esos filtros.")
            lbl.setStyleSheet("color: #5a6b78; font-size: 14px;")
            self.cards_layout.addWidget(lbl)
            self.cards_layout.addStretch()
            return

        for trip in trips:
            card = TripCard(trip, parent=self)
            card.btn_details.clicked.connect(lambda _, t=trip: self.show_trip_details(t))
            self.cards_layout.addWidget(card)

        self.cards_layout.addStretch()

    def show_trip_details(self, trip: Dict):
        info = (
            f"Viaje: {trip.get('trip_id')}\n"
            f"Ruta: {trip.get('route_id')}\n"
            f"Salida: {format_dt(trip.get('departure'))}\n"
            f"Llegada: {format_dt(trip.get('arrival'))}\n"
            f"Origen: {trip.get('origin_city')}\n"
            f"Destino: {trip.get('dest_city')}\n"
            f"Autobús: {trip.get('bus_number')}\n"
            f"Estado: {trip.get('estado_nombre')}\n"
        )
        QMessageBox.information(self, "Detalles del Viaje", info)

    # ---------- DB ----------

    def load_all_trips_from_db(self):
        cur = self.db.cursor(dictionary=True)
        now = datetime.now()

        try:
            cur.execute("""
                SELECT
                    v.numero AS trip_id,
                    v.fecHoraSalida AS departure,
                    v.fecHoraEntrada AS arrival,
                    r.codigo AS route_id,
                    corig.nombre AS origin_city,
                    cdest.nombre AS dest_city,
                    v.autobus AS bus_number,
                    ev.nombre AS estado_nombre
                FROM viaje v
                LEFT JOIN ruta r ON v.ruta = r.codigo
                LEFT JOIN terminal tor ON r.origen = tor.numero
                LEFT JOIN terminal tdest ON r.destino = tdest.numero
                LEFT JOIN ciudad corig ON tor.ciudad = corig.clave
                LEFT JOIN ciudad cdest ON tdest.ciudad = cdest.clave
                LEFT JOIN edo_viaje ev ON v.estado = ev.numero
                ORDER BY v.fecHoraSalida ASC
            """)
            rows = cur.fetchall()

            trips = []
            for row in rows:
                if row["departure"] > now:
                    trip = dict(row)
                    trip["origin_city"] = (row.get("origin_city") or "").strip().title()
                    trip["dest_city"] = (row.get("dest_city") or "").strip().title()
                    trips.append(trip)

            self.all_trips = trips

        finally:
            cur.close()

    # ---------- FILTROS ----------

    def populate_filter_boxes(self):
        origenes = {"Tijuana"}
        destinos = set()

        for t in self.all_trips:
            d = (t.get("dest_city") or "").strip().title()
            destinos.add(d)
            destinos.discard("")

        self.cmb_origen.clear()
        self.cmb_origen.addItems(sorted(origenes))

        self.cmb_dest.clear()
        self.cmb_dest.addItems(["-- Todas --"] + sorted(destinos))

    def apply_filters(self):
        selected_date = self.date_edit.date()
        dest = self.cmb_dest.currentText().strip()
        origen = self.cmb_origen.currentText().strip()

        filtered = self.all_trips

        if self.date_edit.hasFocus() or getattr(self.date_edit, "userChanged", False):
            py_date = selected_date.toPython()
            filtered = [t for t in filtered if t["departure"].date() == py_date]

        if origen and origen != "-- Todas --":
            filtered = [t for t in filtered if t["origin_city"].lower() == origen.lower()]

        if dest and dest != "-- Todas --":
            filtered = [t for t in filtered if t["dest_city"].lower() == dest.lower()]

        self.load_cards(filtered)

    def reset_filters(self):
        self.cmb_origen.setCurrentIndex(0)
        self.cmb_dest.setCurrentIndex(0)
        self.date_edit.userChanged = False

        self.date_edit.blockSignals(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.blockSignals(False)

        self.load_cards(self.all_trips)

    def reload_from_db(self):
        try:
            self.load_all_trips_from_db()
            self.populate_filter_boxes()
            self.load_cards(self.all_trips)
            QMessageBox.information(self, "Actualizado", "Datos actualizados.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar:\n{e}")


# ------------------------ MAIN ------------------------

def main():
    app = QApplication(sys.argv)
    win = ProgramacionWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()