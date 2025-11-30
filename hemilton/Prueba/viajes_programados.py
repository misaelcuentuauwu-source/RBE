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
    QScrollArea, QFrame, QSizePolicy, QDialog
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

        # ------------------------------------------------------------
        #  TÍTULO SUPERIOR (Ejemplo: "Viaje #1 — Ruta #1")
        # ------------------------------------------------------------
        title = QLabel(f"Viaje #{trip.get('trip_id')} — Ruta #{trip.get('route_id')}")
        title.setProperty("class", "title")

        # ------------------------------------------------------------
        #  FILA 1: Salida / Llegada
        # ------------------------------------------------------------
        row1 = QHBoxLayout()
        lbl_salida = QLabel("Salida:")
        lbl_salida.setProperty("class", "label")

        val_salida = QLabel(format_dt(trip.get("departure")))
        val_salida.setProperty("class", "value")

        dot = QLabel("•")
        dot.setStyleSheet("color:#8091a2; font-size:18px;")

        lbl_llegada = QLabel("Llegada:")
        lbl_llegada.setProperty("class", "label")

        val_llegada = QLabel(format_dt(trip.get("arrival")))
        val_llegada.setProperty("class", "value")

        row1.addWidget(lbl_salida)
        row1.addWidget(val_salida)
        row1.addSpacing(25)
        row1.addWidget(dot)
        row1.addSpacing(25)
        row1.addWidget(lbl_llegada)
        row1.addWidget(val_llegada)
        row1.addStretch()


        # ------------------------------------------------------------
        #  FILA 2: Origen → Destino
        # ------------------------------------------------------------
        row2 = QHBoxLayout()
        row2.addWidget(QLabel(trip.get("origin_city",""), objectName="orig")); row2.itemAt(0).widget().setProperty("class", "value")
        arrow = QLabel("  →  "); arrow.setStyleSheet("font-size:16px; color:#1A4A8D;")
        row2.addWidget(arrow)
        row2.addWidget(QLabel(trip.get("dest_city",""), objectName="dest")); row2.itemAt(2).widget().setProperty("class", "value")
        row2.addStretch()

        # ------------------------------------------------------------
        #  FILA 3: Operador
        # ------------------------------------------------------------
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Operador:", objectName="lbl3")); row3.itemAt(0).widget().setProperty("class", "label")
        row3.addWidget(QLabel(trip.get("operator",""), objectName="operator")); row3.itemAt(1).widget().setProperty("class", "value")
        row3.addStretch()

        # ------------------------------------------------------------
        #  FILA 4: Autobús / Placas
        # ------------------------------------------------------------
        row4 = QHBoxLayout()
        row4.addWidget(QLabel("Autobús:", objectName="lbl_bus")); row4.itemAt(0).widget().setProperty("class", "label")
        row4.addWidget(QLabel(str(trip.get("bus_number","")), objectName="bus")); row4.itemAt(1).widget().setProperty("class", "value")
        row4.addSpacing(25)
        row4.addWidget(QLabel("Placas:", objectName="lbl_plate")); row4.itemAt(3).widget().setProperty("class", "label")
        row4.addWidget(QLabel(str(trip.get("plate","")), objectName="plate")); row4.itemAt(4).widget().setProperty("class", "value")
        row4.addStretch()

        # ------------------------------------------------------------
        #  FILA 5: Asientos / Pasajeros
        # ------------------------------------------------------------
        row5 = QHBoxLayout()
        row5.addWidget(QLabel("Asientos:", objectName="lbl_seats")); row5.itemAt(0).widget().setProperty("class", "label")
        row5.addWidget(QLabel(str(trip.get("seats_count","")), objectName="seats")); row5.itemAt(1).widget().setProperty("class", "value")
        row5.addSpacing(25)
        row5.addWidget(QLabel("Pasajeros:", objectName="lbl_pass")); row5.itemAt(3).widget().setProperty("class", "label")
        row5.addWidget(QLabel(str(trip.get("passengers_count","")), objectName="pass")); row5.itemAt(4).widget().setProperty("class", "value")
        row5.addStretch()

        # ------------------------------------------------------------
        #  Botón DETALLES a la derecha
        # ------------------------------------------------------------
        btn_layout = QVBoxLayout()
        self.btn_details = QPushButton("Detalles")
        self.btn_details.setProperty("class", "card-btn")
        btn_layout.addWidget(self.btn_details, alignment=Qt.AlignRight)
        btn_layout.addStretch()

        # ------------------------------------------------------------
        #  Layout principal: datos a la izquierda, botón a la derecha
        # ------------------------------------------------------------
         # ------------------------------------------------------------
        #  ORDEN SOLICITADO — SOLO LO NECESARIO
        # ------------------------------------------------------------

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

        # 3) Ciudad de origen
        origen_lbl = QLabel(f"Origen: {trip.get('origin_city','')}")
        origen_lbl.setProperty("class", "value")
        left.addWidget(origen_lbl)

        # 4) Ciudad de destino
        destino_lbl = QLabel(f"Destino: {trip.get('dest_city','')}")
        destino_lbl.setProperty("class", "value")
        left.addWidget(destino_lbl)
        left.addSpacing(6)

        # 5) Número de autobús
        autobus_lbl = QLabel(f"Autobús: {trip.get('bus_number','')}")
        autobus_lbl.setProperty("class", "value")
        left.addWidget(autobus_lbl)

        left.addStretch()  # Para dejar aire debajo

        main = QHBoxLayout(self)
        main.addLayout(left, 4)
        main.addLayout(btn_layout, 1)

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
    
    # AÑADIR ESTO: Forzar actualización inmediata
    QApplication.processEvents()

    def load_cards(self, trips: List[Dict]):
        self.clear_cards()

        if not trips:
            lbl = QLabel("No hay viajes programados para esos filtros.")
            lbl.setStyleSheet("color: #5a6b78; font-size: 14px;")
            self.cards_layout.addWidget(lbl)
            self.cards_layout.addStretch()
            # AÑADIR: Forzar actualización
            self.cards_container.updateGeometry()
            self.scroll.updateGeometry()
            return

        for trip in trips:
            card = TripCard(trip, parent=self)
            card.btn_details.clicked.connect(lambda _, t=trip: self.show_trip_details(t))
            self.cards_layout.addWidget(card)

        self.cards_layout.addStretch()
        
        # AÑADIR: Forzar actualización del layout
        self.cards_container.updateGeometry()
        self.scroll.widget().adjustSize()
        self.scroll.updateGeometry()
        QApplication.processEvents()  # Procesar eventos pendientes

    def show_trip_details(self, trip: Dict):

        dlg = QDialog(self)
        dlg.setWindowTitle(f"Detalles del Viaje #{trip.get('trip_id')}")
        dlg.resize(850, 500)

        dlg.setStyleSheet("""
            QDialog { background: #f4f7fb; }

            QFrame#detailCard {
                background: white;
                border-radius: 14px;
                border: 1px solid #d6dfe7;
                padding: 22px;
            }

            QLabel.title { 
                font-size: 22px; 
                font-weight: 900; 
                color: #1A4A8D; 
            }
            QLabel.label { 
                font-size: 14px; 
                color: #0b3a66;
                font-weight: 600;
            }
            QLabel.value { 
                font-size: 14px; 
                color: #415466; 
            }

            QPushButton#closeBtn {
                background: #EF6C33;
                color: white;
                padding: 8px 22px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton#closeBtn:hover { background: #d85f2c; }
        """)

        card = QFrame()
        card.setObjectName("detailCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(26)

        # ------------------------
        # BLOQUE 1 - VIAJE Y RUTA
        # ------------------------
        title = QLabel(f"Viaje #{trip.get('trip_id')} — Ruta #{trip.get('route_id')}")
        title.setProperty("class", "title")
        card_layout.addWidget(title)

        # ------------------------
        # BLOQUE 2 - HORAS
        # ------------------------
        horas = QHBoxLayout()
        horas.setSpacing(10)

        col_sal = QVBoxLayout()
        l = QLabel("Hora de salida:"); l.setProperty("class","label")
        v = QLabel(format_dt(trip.get("departure"))); v.setProperty("class","value")
        col_sal.addWidget(l); col_sal.addWidget(v)

        col_lleg = QVBoxLayout()
        l = QLabel("Hora de llegada:"); l.setProperty("class","label")
        v = QLabel(format_dt(trip.get("arrival"))); v.setProperty("class","value")
        col_lleg.addWidget(l); col_lleg.addWidget(v)

        horas.addLayout(col_sal, 1)
        horas.addLayout(col_lleg, 1)
        card_layout.addLayout(horas)

        # ------------------------
        # BLOQUE 3 - ORIGEN / DESTINO
        # ------------------------
        od = QHBoxLayout()
        od.setSpacing(10)

        col_origen = QVBoxLayout()
        for text, val in [
            ("Ciudad de origen:", trip.get("origin_city","")),
            ("Terminal de salida:", trip.get("origin_terminal","")),
        ]:
            l = QLabel(text); l.setProperty("class","label")
            v = QLabel(val);  v.setProperty("class","value")
            col_origen.addWidget(l); col_origen.addWidget(v)

        col_destino = QVBoxLayout()
        for text, val in [
            ("Ciudad de destino:", trip.get("dest_city","")),
            ("Terminal de llegada:", trip.get("dest_terminal","")),
        ]:
            l = QLabel(text); l.setProperty("class","label")
            v = QLabel(val);  v.setProperty("class","value")
            col_destino.addWidget(l); col_destino.addWidget(v)

        od.addLayout(col_origen, 1)
        od.addLayout(col_destino, 1)
        card_layout.addLayout(od)

        # ------------------------
        # BLOQUE 4 - OPERADOR
        # ------------------------
        operador = QVBoxLayout()
        operador.setSpacing(10) 
        l = QLabel("Operador:"); l.setProperty("class","label")
        v = QLabel(trip.get("operator","")); v.setProperty("class","value")
        operador.addWidget(l); operador.addWidget(v)
        card_layout.addLayout(operador)

        # ------------------------
        # BLOQUE 5 - AUTOBÚS (CORREGIDO)
        # ------------------------
        bus_block = QVBoxLayout()
        bus_block.setSpacing(10)

        # Primera fila: Número de autobús | Placas
        row_1 = QHBoxLayout()
        row_1.setSpacing(10)

        col_bus_num = QVBoxLayout()
        l = QLabel("Número de autobús:"); l.setProperty("class","label")
        v = QLabel(str(trip.get("bus_number",""))); v.setProperty("class","value")
        col_bus_num.addWidget(l); col_bus_num.addWidget(v)

        col_placas = QVBoxLayout()
        l = QLabel("Placas:"); l.setProperty("class","label")
        v = QLabel(str(trip.get("plate",""))); v.setProperty("class","value")
        col_placas.addWidget(l); col_placas.addWidget(v)

        row_1.addLayout(col_bus_num, 1)
        row_1.addLayout(col_placas, 1)

        # Segunda fila: Asientos | Pasajeros
        row_2 = QHBoxLayout()
        row_2.setSpacing(10)

        col_asientos = QVBoxLayout()
        l = QLabel("Asientos:"); l.setProperty("class","label")
        v = QLabel(str(trip.get("seats_count",""))); v.setProperty("class","value")
        col_asientos.addWidget(l); col_asientos.addWidget(v)

        col_pasaj = QVBoxLayout()
        l = QLabel("Pasajeros:"); l.setProperty("class","label")
        v = QLabel(str(trip.get("passengers_count",""))); v.setProperty("class","value")
        col_pasaj.addWidget(l); col_pasaj.addWidget(v)

        row_2.addLayout(col_asientos, 1)
        row_2.addLayout(col_pasaj, 1)

        bus_block.addLayout(row_1)
        bus_block.addLayout(row_2)

        card_layout.addLayout(bus_block)

        # Botón cerrar
        btn_close = QPushButton("Cerrar")
        btn_close.setObjectName("closeBtn")
        btn_close.clicked.connect(dlg.close)

        root = QVBoxLayout(dlg)
        root.addWidget(card)
        root.addWidget(btn_close, alignment=Qt.AlignCenter)

        dlg.exec()
        # ---------- DB ----------

    def load_all_trips_from_db(self):
            try:
                self.db.ping(reconnect=True)
            except:
                self.db = crear_conexion()

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

                        CONCAT(c.conNombre, ' ', c.conPrimerApell, ' ', 
                            COALESCE(c.conSegundoApell, '')) AS operator,

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
                now = datetime.now()

                for row in rows:
                    if row["departure"] > now:
                        trip = dict(row)

                        trip["origin_city"] = (row.get("origin_city") or "").title()
                        trip["dest_city"] = (row.get("dest_city") or "").title()

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
        filtered = self.all_trips
        selected_date = self.date_edit.date().toPython()
        origen = self.cmb_origen.currentText().strip()
        dest = self.cmb_dest.currentText().strip()

        # Aplicar filtro de fecha solo si el usuario cambió la fecha
        if getattr(self.date_edit, "userChanged", False):
            filtered = [t for t in filtered if t["departure"].date() == selected_date]

        # Aplicar filtro de origen
        if origen and origen != "-- Todas --":
            filtered = [t for t in filtered if t["origin_city"].lower() == origen.lower()]

        # Aplicar filtro de destino
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
            print("\nACTUALIZANDO DESDE BD...")  # DEBUG
            self.load_all_trips_from_db()
            self.populate_filter_boxes()
            self.load_cards(self.all_trips)
            QMessageBox.information(self, "Actualizado", f"Datos actualizados.\n{len(self.all_trips)} viajes cargados.")
        except Exception as e:
            print(f" Error: {e}")  # DEBUG
            QMessageBox.critical(self, "Error", f"Error al actualizar:\n{e}")


# ------------------------ MAIN ------------------------

def main():
    app = QApplication(sys.argv)
    win = ProgramacionWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()