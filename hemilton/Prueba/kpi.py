# kpi_window.py
import sys
from datetime import datetime, date, time, timedelta
from typing import Optional, Dict, List, Tuple
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QDateEdit, QHBoxLayout, QVBoxLayout,
    QPushButton, QMessageBox, QFrame, QSizePolicy, QSpinBox, QDialog, QTextEdit,QScrollArea,
    QLineEdit
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

from conexion import crear_conexion  # <-- usa tu función existente de conexión MySQL


def format_dt(dt: Optional[datetime]) -> str:
    if dt is None:
        return ""
    if isinstance(dt, str):
        return dt
    return dt.strftime("%Y-%m-%d %H:%M")


# ----------------- Tarjetas -----------------
class TripCardKPI(QFrame):
    """Tarjeta original para Boletos (se conserva)."""
    def __init__(self, trip: dict, parent=None):
        super().__init__(parent)
        self.trip = trip
        self.setObjectName("kpiCard")

        self.setStyleSheet("""
            QFrame#kpiCard {
                background: white;
                border-radius: 16px;
                border: 1px solid #d9d9d9;
            }
            QLabel {
                color: #2c3e50;
                font-size: 15px;
            }
        """)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        main = QVBoxLayout(self)
        main.setContentsMargins(20, 15, 20, 15)
        main.setSpacing(12)

        # --- Fila 1: Fecha programada y número de viaje ---
        row1 = QHBoxLayout()
        row1.setSpacing(25)

        departure = trip.get("departure")
        if isinstance(departure, datetime):
            fecha_prog = departure.strftime("%Y-%m-%d")
            salida_str = departure.strftime("%Y-%m-%d %H:%M")
        else:
            fecha_prog = str(departure)
            salida_str = str(departure)

        lbl_fecha = QLabel(f"Fecha programada: {fecha_prog}")
        lbl_num_viaje = QLabel(f"Número del viaje: {trip.get('trip_id','')}")

        lbl_fecha.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lbl_num_viaje.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        row1.addWidget(lbl_fecha)
        row1.addWidget(lbl_num_viaje)

        # --- Fila 2: Fecha y hora de salida ---
        row2 = QHBoxLayout()
        row2.setSpacing(25)
        lbl_salida = QLabel(f"Fecha y hora de salida: {salida_str}")
        lbl_salida.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        row2.addWidget(lbl_salida)

        # --- Fila 3: Origen / Destino / Autobús ---
        row3 = QHBoxLayout()
        row3.setSpacing(25)

        lbl_origen = QLabel(f"Origen: {trip.get('origin_city','')}")
        lbl_destino = QLabel(f"Destino: {trip.get('dest_city','')}")
        lbl_bus = QLabel(f"Autobús: {trip.get('bus_number','')}")

        for lbl in (lbl_origen, lbl_destino, lbl_bus):
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        row3.addWidget(lbl_origen)
        row3.addWidget(lbl_destino)
        row3.addWidget(lbl_bus)

        # --- Fila 4: Boletos vendidos / disponibles ---
        row4 = QHBoxLayout()
        row4.setSpacing(25)

        lbl_vendidos = QLabel(f"Boletos vendidos: {trip.get('sold_count','')}")
        lbl_disp = QLabel(f"Boletos disponibles: {trip.get('available_count','')}")

        lbl_vendidos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lbl_disp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        row4.addWidget(lbl_vendidos)
        row4.addWidget(lbl_disp)

        # Agregar filas al layout principal
        main.addLayout(row1)
        main.addLayout(row2)
        main.addLayout(row3)
        main.addLayout(row4)

        main.addStretch()


class ConductorCardKPI(QFrame):
    """Tarjeta para KPI de Conductor (incluye matrícula del autobús)."""
    def __init__(self, data: dict, parent=None):
        """
        data keys expected:
        - con_fullname
        - trip_id
        - departure (datetime)
        - arrival (datetime)
        - origin_city
        - dest_city
        - bus_number
        - bus_plates
        """
        super().__init__(parent)
        self.data = data
        self.setObjectName("kpiCardConductor")

        self.setStyleSheet("""
            QFrame#kpiCardConductor {
                background: white;
                border-radius: 16px;
                border: 1px solid #d9d9d9;
            }
            QLabel { color: #2c3e50; font-size: 14.5px; }
        """)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        main = QVBoxLayout(self)
        main.setContentsMargins(18, 12, 18, 12)
        main.setSpacing(10)

        # Row 1: Nombre completo y número de viaje
        r1 = QHBoxLayout()
        lbl_name = QLabel(f"Conductor: {data.get('con_fullname','')}")
        lbl_trip = QLabel(f"Número del viaje: {data.get('trip_id','')}")
        lbl_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lbl_trip.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        r1.addWidget(lbl_name)
        r1.addWidget(lbl_trip)

        # Row 2: Salida / Llegada
        r2 = QHBoxLayout()
        lbl_salida = QLabel(f"Salida: {format_dt(data.get('departure'))}")
        lbl_llegada = QLabel(f"Llegada: {format_dt(data.get('arrival'))}")
        lbl_salida.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lbl_llegada.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        r2.addWidget(lbl_salida)
        r2.addWidget(lbl_llegada)

        # Row 3: Origen / Destino / Autobús (número)
        r3 = QHBoxLayout()
        lbl_origen = QLabel(f"Origen: {data.get('origin_city','')}")
        lbl_destino = QLabel(f"Destino: {data.get('dest_city','')}")
        lbl_bus = QLabel(f"Autobús: {data.get('bus_number','')}")
        for lbl in (lbl_origen, lbl_destino, lbl_bus):
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        r3.addWidget(lbl_origen)
        r3.addWidget(lbl_destino)
        r3.addWidget(lbl_bus)

        # Row 4: Matricula
        r4 = QHBoxLayout()
        lbl_placas = QLabel(f"Matrícula: {data.get('bus_plates','')}")
        lbl_placas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        r4.addWidget(lbl_placas)

        main.addLayout(r1)
        main.addLayout(r2)
        main.addLayout(r3)
        main.addLayout(r4)
        main.addStretch()


class AutobusCardKPI(QFrame):
    """Tarjeta para Autobús con botón Detalles."""
    def __init__(self, data: dict, parent=None, db_conn=None):
        """
        data keys expected:
        - bus_number
        - placas
        - marca_nombre
        - modelo_nombre
        - modelo_año
        - numasientos
        """
        super().__init__(parent)
        self.data = data
        self.db_conn = db_conn
        self.setObjectName("kpiCardAutobus")

        self.setStyleSheet("""
            QFrame#kpiCardAutobus {
                background: white;
                border-radius: 16px;
                border: 1px solid #d9d9d9;
            }
            QLabel { color: #2c3e50; font-size: 14.5px; }
            QPushButton { background: #EF6C33; color: white; border-radius:8px; padding:6px 8px; font-weight:bold; }
        """)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        main = QVBoxLayout(self)
        main.setContentsMargins(18, 12, 18, 12)
        main.setSpacing(10)

        # Row 1: Numero / placas
        r1 = QHBoxLayout()
        lbl_num = QLabel(f"Autobús: {data.get('bus_number','')}")
        lbl_placa = QLabel(f"Matrícula: {data.get('placas','')}")
        lbl_num.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lbl_placa.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        r1.addWidget(lbl_num)
        r1.addWidget(lbl_placa)

        # Row 2: Marca / Modelo
        r2 = QHBoxLayout()
        lbl_marca = QLabel(f"Marca: {data.get('marca_nombre','')}")
        lbl_modelo = QLabel(f"Modelo: {data.get('modelo_nombre','')}")
        lbl_marca.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lbl_modelo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        r2.addWidget(lbl_marca)
        r2.addWidget(lbl_modelo)

        # Row 3: Año / Cantidad de asientos + Detalles label (botón)
        r3 = QHBoxLayout()
        lbl_año = QLabel(f"Año: {data.get('modelo_año','')}")
        lbl_asientos = QLabel(f"Asientos: {data.get('numasientos','')}")
        lbl_año.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lbl_asientos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        btn_detalles = QPushButton("Detalles")
        btn_detalles.setFixedWidth(110)
        btn_detalles.clicked.connect(self._on_detalles)
        r3.addWidget(lbl_año)
        r3.addWidget(lbl_asientos)
        r3.addWidget(btn_detalles)

        main.addLayout(r1)
        main.addLayout(r2)
        main.addLayout(r3)
        main.addStretch()

    def _on_detalles(self):
        """Abre modal con descripción por tipo de asiento y cantidad por tipo para este autobús."""
        bus_num = self.data.get("bus_number")
        if not bus_num:
            QMessageBox.information(self, "Detalles", "No hay información de autobús.")
            return

        # Query tipos y conteo
        try:
            db = self.db_conn
            try:
                cur = db.cursor(dictionary=True)
            except TypeError:
                cur = db.cursor()
            cur.execute("""
                SELECT ta.descripcion AS tipo_desc, COUNT(*) AS cantidad
                FROM asiento a
                JOIN tipo_asiento ta ON a.tipo = ta.codigo
                WHERE a.autobus = %s
                GROUP BY ta.descripcion
            """, (bus_num,))
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar detalles:\n{e}")
            return
        finally:
            try:
                cur.close()
            except:
                pass

        dlg = QDialog(self)
        dlg.setWindowTitle(f"Detalles - Autobús {bus_num}")
        dlg.setModal(True)
        form = QVBoxLayout(dlg)
        # Descripción general
        desc = QTextEdit()
        desc.setReadOnly(True)
        lines = []
        lines.append(f"Autobús: {bus_num}")
        lines.append(f"Matrícula: {self.data.get('placas','')}")
        lines.append("")
        lines.append("Tipos de asiento y cantidades:")
        for r in rows:
            lines.append(f" - {r.get('tipo_desc')}: {r.get('cantidad')}")
        desc.setText("\n".join(lines))

        form.addWidget(desc)
        dlg.setLayout(form)
        dlg.exec()


class CiudadCardKPI(QFrame):
    """Tarjeta para Ciudad KPI."""
    def __init__(self, data: dict, parent=None):
        """
        data keys expected:
        - city_name
        - departure
        - trip_id
        - dest_city
        - bus_number
        - bus_plates
        - operator_fullname
        """
        super().__init__(parent)
        self.data = data
        self.setObjectName("kpiCardCiudad")

        self.setStyleSheet("""
            QFrame#kpiCardCiudad {
                background: white;
                border-radius: 16px;
                border: 1px solid #d9d9d9;
            }
            QLabel { color: #2c3e50; font-size: 14.5px; }
        """)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        main = QVBoxLayout(self)
        main.setContentsMargins(18, 12, 18, 12)
        main.setSpacing(10)

        r1 = QHBoxLayout()
        lbl_city = QLabel(f"Ciudad: {data.get('city_name','')}")
        lbl_dest = QLabel(f"Destino: {data.get('dest_city','')}")
        lbl_city.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lbl_dest.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        r1.addWidget(lbl_city)
        r1.addWidget(lbl_dest)

        r2 = QHBoxLayout()
        lbl_salida = QLabel(f"Salida: {format_dt(data.get('departure'))}")
        lbl_corrida = QLabel(f"Corrida: {data.get('trip_id','')}")
        lbl_salida.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lbl_corrida.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        r2.addWidget(lbl_salida)
        r2.addWidget(lbl_corrida)

        r3 = QHBoxLayout()
        lbl_bus = QLabel(f"Autobús: {data.get('bus_number','')}")
        lbl_placa = QLabel(f"Matrícula: {data.get('bus_plates','')}")
        lbl_oper = QLabel(f"Operador: {data.get('operator_fullname','')}")
        for lbl in (lbl_bus, lbl_placa, lbl_oper):
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        r3.addWidget(lbl_bus)
        r3.addWidget(lbl_placa)
        r3.addWidget(lbl_oper)

        main.addLayout(r1)
        main.addLayout(r2)
        main.addLayout(r3)
        main.addStretch()


# ----------------- Ventana Principal -----------------
class KPIWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KPI - Viajes (Tarjeta única)")
        self.resize(980, 500)

        try:
            self.db = crear_conexion()
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"No se pudo conectar a la BD:\n{e}")
            raise

        # state flags
        self.initial_load = True      # para que Boletos muestre todo al inicio
        self.apply_pressed = False    # indica si el usuario presionó Aplicar alguna vez

        # ---- Filtro maestro: Qué KPI mostrar ----
        lbl_tipo = QLabel("Ver:")
        self.cmb_tipo = QComboBox()
        self.cmb_tipo.addItems(["Boletos", "Conductor", "Autobús", "Ciudad"])
        self.cmb_tipo.currentIndexChanged.connect(self.on_tipo_changed)

        # ---- Filtros (alcance temporal) ----
        lbl_scope = QLabel("Filtro:")
        self.cmb_scope = QComboBox()
        self.cmb_scope.addItems(["Día", "Semana (actual)", "Mes"])
        self.cmb_scope.currentIndexChanged.connect(self._on_scope_changed)

        # Para Día
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMinimumWidth(130)

        # Para Mes (mes + año)
        self.cmb_month = QComboBox()
        months = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self.cmb_month.addItems(months)
        self.cmb_year = QSpinBox()
        self.cmb_year.setRange(2000, 2100)
        self.cmb_year.setValue(QDate.currentDate().year())
        self.cmb_month.setCurrentIndex(QDate.currentDate().month()-1)

        # Botones
        self.btn_apply = QPushButton("Aplicar")
        self.btn_apply.clicked.connect(self.on_apply_clicked)

        self.btn_reload = QPushButton("Actualizar BD")
        self.btn_reload.clicked.connect(self.reload_from_db)

        # --- Filtros específicos por KPI (opción C) ---
        # Conductor: búsqueda por nombre
        self.lbl_search_conductor = QLabel("Buscar conductor:")
        self.edit_search_conductor = QLineEdit()
        self.edit_search_conductor.setPlaceholderText("Nombre o apellido")
        self.edit_search_conductor.returnPressed.connect(self.apply_filters)

        # Autobús: número de autobús exacto (puede ser string)
        self.lbl_search_bus = QLabel("Número de autobús:")
        self.edit_search_bus = QLineEdit()
        self.edit_search_bus.setPlaceholderText("Ej: 501")
        self.edit_search_bus.returnPressed.connect(self.apply_filters)

        # Ciudad: ciudad destino parcial
        self.lbl_search_city = QLabel("Ciudad destino:")
        self.edit_search_city = QLineEdit()
        self.edit_search_city.setPlaceholderText("Ej: Ensenada")
        self.edit_search_city.returnPressed.connect(self.apply_filters)

        # Contenedor tarjeta con scroll
       

        # Contenedor tarjeta con scroll

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("border: none;")  # opcional, estético

        self.card_frame = QFrame()
        self.card_layout = QVBoxLayout(self.card_frame)

        self.scroll.setWidget(self.card_frame)

        self.card_frame = QFrame()
        self.card_layout = QVBoxLayout(self.card_frame)

        self.scroll.setWidget(self.card_frame)

        # Info adicional (cantidad de resultados)
        self.lbl_info = QLabel("")
        self.lbl_info.setStyleSheet("color: #5a6b78; font-weight:600;")

        # Layout superior de controles (tipo arriba)
        controls = QHBoxLayout()
        controls.addWidget(lbl_tipo)
        controls.addWidget(self.cmb_tipo)
        controls.addSpacing(20)

        controls.addWidget(lbl_scope)
        controls.addWidget(self.cmb_scope)
        controls.addSpacing(8)
        controls.addWidget(self.date_edit)
        controls.addSpacing(6)
        controls.addWidget(self.cmb_month)
        controls.addWidget(self.cmb_year)
        controls.addSpacing(10)

        # place for KPI-specific filters (we'll manage visibility)
        controls.addWidget(self.lbl_search_conductor)
        controls.addWidget(self.edit_search_conductor)
        controls.addWidget(self.lbl_search_bus)
        controls.addWidget(self.edit_search_bus)
        controls.addWidget(self.lbl_search_city)
        controls.addWidget(self.edit_search_city)

        controls.addWidget(self.btn_apply)
        controls.addWidget(self.btn_reload)
        controls.addStretch()

        # Root layout
        root = QVBoxLayout(self)
        root.addLayout(controls)
        root.addSpacing(8)
        root.addWidget(self.lbl_info)
        root.addWidget(self.scroll)
        root.addStretch()

        # Estado
        self.all_trips = []
        self.load_all_trips_from_db()   # usado por Boletos
        self._on_scope_changed()   # ajusta visibilidad controles

        # Ocultar los filtros específicos por defecto
        self._update_filter_visibility()

        # primer render
        self.apply_filters()

        # estilos simples
        self.setStyleSheet("""
            QLabel { color: #0b3a66; font-weight: 600; }
            QPushButton { background: #EF6C33; color: white; border-radius:8px; padding:6px 10px; font-weight:bold; }
            QPushButton:hover { background:#d85f2c; }
            QComboBox, QDateEdit, QSpinBox, QLineEdit { padding:6px 8px; border-radius:8px; border:1px solid #cbd7e6; background:#fff; }
        """)

    # ---------------- DB ----------------
    def load_all_trips_from_db(self):
        """
        Carga en memoria todos los viajes (futuros y pasados). Filtrado y selección posterior
        se hace en Python/SQL según el scope.
        """
        try:
            self.db.ping(reconnect=True)
        except:
            self.db = crear_conexion()

        try:
            cur = self.db.cursor(dictionary=True)
        except TypeError:
            cur = self.db.cursor()
        try:
            cur.execute("""
                SELECT
                    v.numero AS trip_id,
                    v.fecHoraSalida AS departure,
                    v.fecHoraEntrada AS arrival,
                    r.origen AS origin_terminal_num,
                    tor.nombre AS origin_terminal,
                    corig.nombre AS origin_city,
                    r.destino AS dest_terminal_num,
                    tdest.nombre AS dest_terminal,
                    cdest.nombre AS dest_city,
                    v.autobus AS bus_number,
                    mo.numasientos AS seats_count
                FROM viaje v
                LEFT JOIN ruta r ON v.ruta = r.codigo
                LEFT JOIN terminal tor ON r.origen = tor.numero
                LEFT JOIN terminal tdest ON r.destino = tdest.numero
                LEFT JOIN ciudad corig ON tor.ciudad = corig.clave
                LEFT JOIN ciudad cdest ON tdest.ciudad = cdest.clave
                LEFT JOIN autobus a ON v.autobus = a.numero
                LEFT JOIN modelo mo ON a.modelo = mo.numero
                ORDER BY v.fecHoraSalida ASC
            """)
            rows = cur.fetchall()
            trips = []
            for row in rows:
                trips.append(dict(row))
            self.all_trips = trips
        finally:
            try:
                cur.close()
            except:
                pass

    # ---------------- filtros y helpers ----------------
    def _on_scope_changed(self):
        idx = self.cmb_scope.currentIndex()
        # 0=Día, 1=Semana, 2=Mes
        self.date_edit.setVisible(idx == 0)
        self.cmb_month.setVisible(idx == 2)
        self.cmb_year.setVisible(idx == 2)

    def on_tipo_changed(self):
        # cada vez que cambia el KPI, actualizamos qué filtros se muestran
        self._update_filter_visibility()
        # reset apply flag so user can filter again if desired
        # (we keep initial_load logic only for boletos)
        self.apply_filters()

    def _update_filter_visibility(self):
        tipo = self.cmb_tipo.currentText()
        # hide all
        self.lbl_search_conductor.setVisible(False)
        self.edit_search_conductor.setVisible(False)
        self.lbl_search_bus.setVisible(False)
        self.edit_search_bus.setVisible(False)
        self.lbl_search_city.setVisible(False)
        self.edit_search_city.setVisible(False)

        # show depending on tipo
        if tipo == "Conductor":
            self.lbl_search_conductor.setVisible(True)
            self.edit_search_conductor.setVisible(True)
        elif tipo == "Autobús":
            self.lbl_search_bus.setVisible(True)
            self.edit_search_bus.setVisible(True)
        elif tipo == "Ciudad":
            self.lbl_search_city.setVisible(True)
            self.edit_search_city.setVisible(True)

    def on_apply_clicked(self):
        # mark that apply was explicitly requested
        self.apply_pressed = True
        # After first explicit apply, we consider initial load finished
        self.initial_load = False
        self.apply_filters()

    def apply_filters(self):
        """
        Router: según tipo de KPI seleccionado, llama a la función correspondiente.
        """
        tipo = self.cmb_tipo.currentText()
        # limpiar primero
        self.clear_card()

        if tipo == "Boletos":
            return self._apply_kpi_boletos()
        elif tipo == "Conductor":
            return self._apply_kpi_conductor()
        elif tipo == "Autobús":
            return self._apply_kpi_autobus()
        elif tipo == "Ciudad":
            return self._apply_kpi_ciudad()
        else:
            self.lbl_info.setText("Tipo desconocido.")
            return

    # ---------------- KPI: Boletos (mantengo tu lógica original con ajuste inicial) ----------------
    def _apply_kpi_boletos(self):
        # if initial_load True -> load ALL trips (past, present, future)
        if self.initial_load:
            filtered = self.all_trips[:]
        else:
            # compute date range from controls
            rng = self._compute_date_range()
            if rng is None:
                return
            start, end = rng
            filtered = [
                t for t in self.all_trips
                if isinstance(t.get("departure"), datetime)
                and start <= t["departure"] <= end
            ]

        total = len(filtered)
        self.lbl_info.setText(f"Resultados: {total} viaje(s).")

        # Si no hay viajes
        if not filtered:
            lbl = QLabel("No hay viajes para el filtro seleccionado.")
            lbl.setStyleSheet("color:#5a6b78; font-size:14px;")
            self.card_layout.addWidget(lbl)
            return

        # Crear una tarjeta por cada viaje (con stats)
        try:
            for trip in filtered:
                stats = self._fetch_ticket_stats(trip["trip_id"], trip.get("seats_count") or 0)
                trip["sold_count"] = stats["sold"]
                trip["available_count"] = stats["available"]

                # Convertir fecha si viene string
                if isinstance(trip.get("departure"), str):
                    try:
                        trip["departure"] = datetime.fromisoformat(trip["departure"])
                    except:
                        pass

                card = TripCardKPI(trip, parent=self)
                self.card_layout.addWidget(card)
            self.card_layout.addStretch()
            # after first render, initial_load should be False when user later presses apply
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al renderizar KPI Boletos: {e}")

    def _fetch_ticket_stats(self, viaje_id: int, seats_count: int) -> Dict[str,int]:
        sold = 0
        try:
            cur = self.db.cursor()
        except TypeError:
            cur = self.db.cursor(dictionary=True)
        try:
            cur.execute("SELECT COUNT(*) FROM ticket WHERE viaje = %s", (viaje_id,))
            res = cur.fetchone()
            if res:
                sold = int(res[0]) if isinstance(res, (list, tuple)) else int(list(res.values())[0])
        except Exception as e:
            print("Error al obtener tickets:", e)
        finally:
            try:
                cur.close()
            except:
                pass

        available = seats_count - sold if seats_count and seats_count >= sold else max(0, seats_count - sold) if seats_count else 0
        return {"sold": sold, "available": available}

    # ---------------- KPI: Conductor ----------------
    def _apply_kpi_conductor(self):
        """
        Consulta los viajes (conductor) y permite filtro por nombre del conductor y por rango de fechas (si apply_pressed True).
        """
        # build base query and params
        where_clauses = []
        params = []

        # if user pressed apply -> restrict by date range
        if self.apply_pressed:
            rng = self._compute_date_range()
            if rng is None:
                return
            start, end = rng
            where_clauses.append("v.fecHoraSalida BETWEEN %s AND %s")
            params.extend([start, end])

        # conductor name filter
        name_filter = self.edit_search_conductor.text().strip()
        if name_filter:
            # search across conNombre, conPrimerApell, conSegundoApell
            where_clauses.append("(c.conNombre LIKE %s OR c.conPrimerApell LIKE %s OR c.conSegundoApell LIKE %s)")
            likeval = f"%{name_filter}%"
            params.extend([likeval, likeval, likeval])

        where_sql = " AND ".join(where_clauses)
        if where_sql:
            where_sql = "WHERE " + where_sql

        try:
            try:
                cur = self.db.cursor(dictionary=True)
            except TypeError:
                cur = self.db.cursor()
            sql = f"""
                SELECT
                    v.numero AS trip_id,
                    v.fecHoraSalida AS departure,
                    v.fecHoraEntrada AS arrival,
                    corig.nombre AS origin_city,
                    cdest.nombre AS dest_city,
                    v.autobus AS bus_number,
                    a.placas AS bus_plates,
                    c.conNombre AS con_nombre,
                    c.conPrimerApell AS con_ap1,
                    c.conSegundoApell AS con_ap2
                FROM viaje v
                LEFT JOIN ruta r ON v.ruta = r.codigo
                LEFT JOIN terminal tor ON r.origen = tor.numero
                LEFT JOIN terminal tdest ON r.destino = tdest.numero
                LEFT JOIN ciudad corig ON tor.ciudad = corig.clave
                LEFT JOIN ciudad cdest ON tdest.ciudad = cdest.clave
                LEFT JOIN autobus a ON v.autobus = a.numero
                LEFT JOIN conductor c ON v.conductor = c.registro
                {where_sql}
                ORDER BY v.fecHoraSalida ASC
            """
            cur.execute(sql, tuple(params) if params else None)
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"No se pudo leer conductores: {e}")
            try:
                cur.close()
            finally:
                pass
            return
        finally:
            try:
                cur.close()
            except:
                pass

        if not rows:
            lbl = QLabel("No hay viajes para el filtro seleccionado.")
            lbl.setStyleSheet("color:#5a6b78; font-size:14px;")
            self.card_layout.addWidget(lbl)
            return

        total = len(rows)
        self.lbl_info.setText(f"Resultados: {total} viaje(s).")

        for r in rows:
            fullname = " ".join(filter(None, [r.get("con_nombre") or "", r.get("con_ap1") or "", r.get("con_ap2") or ""])).strip()
            data = {
                "con_fullname": fullname,
                "trip_id": r.get("trip_id"),
                "departure": r.get("departure"),
                "arrival": r.get("arrival"),
                "origin_city": r.get("origin_city"),
                "dest_city": r.get("dest_city"),
                "bus_number": r.get("bus_number"),
                "bus_plates": r.get("bus_plates")
            }
            card = ConductorCardKPI(data, parent=self)
            self.card_layout.addWidget(card)
        self.card_layout.addStretch()

    # ---------------- KPI: Autobús ----------------
    def _apply_kpi_autobus(self):
        """
        Lista autobuses (filtrados por viajes en el rango si apply_pressed True) y por número si se ingresó.
        """
        where_clauses = []
        params = []

        # If apply pressed, limit by date
        if self.apply_pressed:
            rng = self._compute_date_range()
            if rng is None:
                return
            start, end = rng
            where_clauses.append("v.fecHoraSalida BETWEEN %s AND %s")
            params.extend([start, end])

        # bus number filter
        bus_filter = self.edit_search_bus.text().strip()
        if bus_filter:
            # try to interpret as int; if not, will match string field a.numero
            try:
                bus_num = int(bus_filter)
                where_clauses.append("a.numero = %s")
                params.append(bus_num)
            except:
                # no conversion: compare as string on placas or number cast
                where_clauses.append("(a.numero = %s OR a.placas LIKE %s)")
                params.append(bus_filter)
                params.append(f"%{bus_filter}%")

        where_sql = " AND ".join(where_clauses)
        if where_sql:
            where_sql = "WHERE " + where_sql

        try:
            try:
                cur = self.db.cursor(dictionary=True)
            except TypeError:
                cur = self.db.cursor()
            sql = f"""
                SELECT DISTINCT
                    a.numero AS bus_number,
                    a.placas AS placas,
                    mo.nombre AS modelo_nombre,
                    mo.año AS modelo_año,
                    mo.numasientos AS numasientos,
                    m.nombre AS marca_nombre
                FROM viaje v
                JOIN autobus a ON v.autobus = a.numero
                LEFT JOIN modelo mo ON a.modelo = mo.numero
                LEFT JOIN marca m ON mo.marca = m.numero
                {where_sql}
                ORDER BY a.numero ASC
            """
            cur.execute(sql, tuple(params) if params else None)
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"No se pudo leer autobuses: {e}")
            try:
                cur.close()
            finally:
                pass
            return
        finally:
            try:
                cur.close()
            except:
                pass

        if not rows:
            lbl = QLabel("No hay autobuses con viajes en el rango (o que cumplan el filtro).")
            lbl.setStyleSheet("color:#5a6b78; font-size:14px;")
            self.card_layout.addWidget(lbl)
            return

        total = len(rows)
        self.lbl_info.setText(f"Resultados: {total} autobús(es).")

        for r in rows:
            data = {
                "bus_number": r.get("bus_number"),
                "placas": r.get("placas"),
                "marca_nombre": r.get("marca_nombre"),
                "modelo_nombre": r.get("modelo_nombre"),
                "modelo_año": r.get("modelo_año"),
                "numasientos": r.get("numasientos")
            }
            card = AutobusCardKPI(data, parent=self, db_conn=self.db)
            self.card_layout.addWidget(card)
        self.card_layout.addStretch()

    # ---------------- KPI: Ciudad ----------------
    def _apply_kpi_ciudad(self):
        """
        Lista viajes agrupados por la ciudad de origen (o cada viaje como tarjeta) con filtro opcional por ciudad destino.
        """
        where_clauses = []
        params = []

        # date range only if apply pressed
        if self.apply_pressed:
            rng = self._compute_date_range()
            if rng is None:
                return
            start, end = rng
            where_clauses.append("v.fecHoraSalida BETWEEN %s AND %s")
            params.extend([start, end])

        # destination city filter
        city_filter = self.edit_search_city.text().strip()
        if city_filter:
            where_clauses.append("cdest.nombre LIKE %s")
            params.append(f"%{city_filter}%")

        where_sql = " AND ".join(where_clauses)
        if where_sql:
            where_sql = "WHERE " + where_sql

        try:
            try:
                cur = self.db.cursor(dictionary=True)
            except TypeError:
                cur = self.db.cursor()
            sql = f"""
                SELECT
                    corig.nombre AS city_name,
                    v.fecHoraSalida AS departure,
                    v.numero AS trip_id,
                    cdest.nombre AS dest_city,
                    v.autobus AS bus_number,
                    a.placas AS bus_plates,
                    c.conNombre AS con_nombre,
                    c.conPrimerApell AS con_ap1,
                    c.conSegundoApell AS con_ap2
                FROM viaje v
                LEFT JOIN ruta r ON v.ruta = r.codigo
                LEFT JOIN terminal tor ON r.origen = tor.numero
                LEFT JOIN terminal tdest ON r.destino = tdest.numero
                LEFT JOIN ciudad corig ON tor.ciudad = corig.clave
                LEFT JOIN ciudad cdest ON tdest.ciudad = cdest.clave
                LEFT JOIN autobus a ON v.autobus = a.numero
                LEFT JOIN conductor c ON v.conductor = c.registro
                {where_sql}
                ORDER BY v.fecHoraSalida ASC
            """
            cur.execute(sql, tuple(params) if params else None)
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"No se pudo leer ciudades: {e}")
            try:
                cur.close()
            finally:
                pass
            return
        finally:
            try:
                cur.close()
            except:
                pass

        if not rows:
            lbl = QLabel("No hay viajes para el filtro seleccionado.")
            lbl.setStyleSheet("color:#5a6b78; font-size:14px;")
            self.card_layout.addWidget(lbl)
            return

        total = len(rows)
        self.lbl_info.setText(f"Resultados: {total} viaje(s).")

        for r in rows:
            fullname = " ".join(filter(None, [r.get("con_nombre") or "", r.get("con_ap1") or "", r.get("con_ap2") or ""])).strip()
            data = {
                "city_name": r.get("city_name"),
                "departure": r.get("departure"),
                "trip_id": r.get("trip_id"),
                "dest_city": r.get("dest_city"),
                "bus_number": r.get("bus_number"),
                "bus_plates": r.get("bus_plates"),
                "operator_fullname": fullname
            }
            card = CiudadCardKPI(data, parent=self)
            self.card_layout.addWidget(card)
        self.card_layout.addStretch()

    # ---------------- Helpers ----------------
    def _compute_date_range(self) -> Optional[Tuple[datetime, datetime]]:
        """Retorna (start, end) según los controles; muestra mensajes si hay problema."""
        scope = self.cmb_scope.currentText()
        try:
            if scope == "Día":
                qdate = self.date_edit.date().toPython()
                start = datetime.combine(qdate, time.min)
                end = datetime.combine(qdate, time.max)
            elif scope == "Semana (actual)":
                today = date.today()
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                start = datetime.combine(start_of_week, time.min)
                end = datetime.combine(end_of_week, time.max)
            else:  # Mes
                month_index = self.cmb_month.currentIndex() + 1
                year = int(self.cmb_year.value())
                start = datetime(year, month_index, 1, 0, 0, 0)
                if month_index == 12:
                    end = datetime(year, 12, 31, 23, 59, 59)
                else:
                    next_month = datetime(year, month_index + 1, 1)
                    end = next_month - timedelta(seconds=1)
            return start, end
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo calcular el rango de fechas: {e}")
            return None

    def clear_card(self):
        while self.card_layout.count():
            item = self.card_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def reload_from_db(self):
        try:
            # reload trips and run same view
            self.load_all_trips_from_db()
            self.apply_filters()
            QMessageBox.information(self, "Actualizado", f"Datos actualizados.\n{len(self.all_trips)} viajes cargados.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar:\n{e}")


# ----------------- Ejecución directa -----------------
def main():
    app = QApplication(sys.argv)
    win = KPIWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()