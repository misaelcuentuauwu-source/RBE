# kpi_window.py
import sys
from datetime import datetime, date, time, timedelta
from typing import Optional, Dict, List, Tuple
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QDateEdit, QHBoxLayout, QVBoxLayout,
    QPushButton, QMessageBox, QFrame, QSizePolicy, QSpinBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog, QDialog
)
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtCore import Qt, QDate
from conexion import crear_conexion  # <-- usa tu función existente de conexión MySQL

def format_dt(dt: Optional[datetime]) -> str:
    if dt is None:
        return ""
    if isinstance(dt, str):
        return dt
    return dt.strftime("%Y-%m-%d %H:%M")


class KPIWindow(QWidget):
    """
    Versión de KPI convertida a TABLA (estilo RBE: azul + naranja).
    Soporta las mismas vistas: Boletos, Conductor, Autobús, Ciudad.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("KPI - Viajes (Tablas)")
        self.resize(1100, 640)

        try:
            self.db = crear_conexion()
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"No se pudo conectar a la BD:\n{e}")
            raise

        # state flags
        self.initial_load = True      # para Boletos mostrar todo al inicio
        self.apply_pressed = False    # indica si el usuario presionó Aplicar alguna vez

        # ---- Controles superiores ----
        lbl_tipo = QLabel("Ver:")
        self.cmb_tipo = QComboBox()
        self.cmb_tipo.addItems(["Boletos", "Conductor", "Autobús", "Ciudad"])
        self.cmb_tipo.currentIndexChanged.connect(self.on_tipo_changed)

        lbl_scope = QLabel("Filtro:")
        self.cmb_scope = QComboBox()
        self.cmb_scope.addItems(["Día", "Semana (actual)", "Mes","Cualquiera"])
        self.cmb_scope.currentIndexChanged.connect(self._on_scope_changed)

        # Fecha (día)
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMinimumWidth(130)

        # Mes/año
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

        # Filtros por KPI
        self.lbl_search_conductor = QLabel("Filtrar conductor:")
        self.cmb_conductor = QComboBox()
        self.cmb_conductor.setMinimumWidth(200)
        self.cmb_conductor.addItem("Todos", None)

        self.lbl_search_bus = QLabel("Filtrar autobús:")
        self.cmb_bus = QComboBox()
        self.cmb_bus.setMinimumWidth(200)
        self.cmb_bus.addItem("Todos", None)

        self.lbl_search_city = QLabel("Filtrar ciudad origen:")
        self.cmb_city = QComboBox()
        self.cmb_city.setMinimumWidth(200)
        self.cmb_city.addItem("Todas", None)

        # Tabla central que mostrará los datos
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.table.cellClicked.connect(self.on_cell_clicked)
        # Preferencias del usuario (según tus respuestas):
        # 1) Ordenar columnas -> NO
        self.table.setSortingEnabled(False)
        # 2) Scroll horizontal -> NO (preferimos estirar columnas)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 3) Columnas se estiren automáticamente -> SÍ
        # 4) Selección de filas completas -> NO (dejamos selección por celdas)
        self.table.setSelectionBehavior(QAbstractItemView.SelectItems)

        # Botón exportar (exporta lo visible)
        self.btn_export = QPushButton("Exportar CSV")
        self.btn_export.clicked.connect(self.export_table_csv)

        # Info adicional
        self.lbl_info = QLabel("")
        self.lbl_info.setStyleSheet("color: #5a6b78; font-weight:600;")

        # Layouts
        top_controls = QHBoxLayout()
        top_controls.addWidget(lbl_tipo)
        top_controls.addWidget(self.cmb_tipo)
        top_controls.addSpacing(16)
        top_controls.addWidget(lbl_scope)
        top_controls.addWidget(self.cmb_scope)
        top_controls.addWidget(self.date_edit)
        top_controls.addWidget(self.cmb_month)
        top_controls.addWidget(self.cmb_year)
        top_controls.addSpacing(8)
        top_controls.addWidget(self.btn_apply)
        top_controls.addWidget(self.btn_reload)
        top_controls.addStretch()

        filters_layout = QHBoxLayout()
        filters_layout.addWidget(self.lbl_search_conductor)
        filters_layout.addWidget(self.cmb_conductor)
        filters_layout.addSpacing(12)
        filters_layout.addWidget(self.lbl_search_bus)
        filters_layout.addWidget(self.cmb_bus)
        filters_layout.addSpacing(12)
        filters_layout.addWidget(self.lbl_search_city)
        filters_layout.addWidget(self.cmb_city)
        filters_layout.addStretch()
        filters_layout.addWidget(self.btn_export)

        root = QVBoxLayout(self)
        root.addLayout(top_controls)
        root.addLayout(filters_layout)
        root.addWidget(self.lbl_info)
        root.addWidget(self.table)

        # Estado / datos en memoria
        self.all_trips = []
        self.load_all_trips_from_db()   # usado por Boletos
        self._on_scope_changed()        # ajusta visibilidad controles
        self.load_conductores()
        self.load_autobuses()
        self.load_ciudades()
        self._update_filter_visibility()

        # estilos (RBE - azul + naranja)
        self.setStyleSheet("""
            QWidget { background: #eef4fb; color: #0b3a66; font-weight: 600; }
            QLabel { color: #0b3a66; font-weight: 600; }
            QPushButton {
                background: #EF6C33;
                color: white;
                border-radius:8px;
                padding:6px 10px;
                font-weight:bold;
            }
            QPushButton:hover { background:#d85f2c; }
            QComboBox, QDateEdit, QSpinBox {
                padding:6px 8px;
                border-radius:6px;
                border:1px solid #cbd7e6;
                background:#fff;
            }
            QTableWidget {
                background: white;
                gridline-color: #e6eef8;
                border: 1px solid #d6e6fb;
                selection-background-color: #EF6C33; /* naranja RBE */
                selection-color: white;
            }
            QHeaderView::section {
                background: #1A4A8D; /* azul RBE */
                color: white;
                padding: 6px;
                border: none;
                font-weight: 700;
            }
            QTableWidget::item {
                padding: 6px;
            }
        """)

        # primer render
        self.apply_filters()


    def on_cell_clicked(self, row, column):
        # ¿Clic en la columna de Asientos?
        if hasattr(self, "asientos_column_index") and column == self.asientos_column_index:
            item = self.table.item(row, column)
            if not item:
                return

            # Obtener el numero del autobus desde la tabla (columna 0 normalmente)
            autobus_num = self.table.item(row, 0).text()

            # ================================
            #   CONSULTA A LA BASE DE DATOS
            # ================================
            try:
                cn = crear_conexion()
                cur = cn.cursor(dictionary=True)

                cur.execute("""
                    SELECT 
                        a.numero AS autobus_numero,
                        ta.descripcion AS tipo_asiento,
                        COUNT(*) AS cantidad
                    FROM asiento s
                    JOIN tipo_asiento ta ON s.tipo = ta.codigo
                    JOIN autobus a ON s.autobus = a.numero
                    WHERE a.numero = %s
                    GROUP BY a.numero, ta.descripcion
                """, (autobus_num,))

                detalles = cur.fetchall()

                cur.close()
                cn.close()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo obtener los asientos: {e}")
                return

            # ================================
            #     CREAR EL POPUP BONITO
            # ================================
            dlg = QDialog(self)
            dlg.setWindowTitle(f"Detalles de Asientos - Autobús {autobus_num}")
            dlg.resize(350, 200)

            layout = QVBoxLayout(dlg)

            # Construimos el texto final
            texto = f"<b>Autobús {autobus_num}</b><br><br>"

            for d in detalles:
                texto += f"• <b>{d['tipo_asiento']}</b>: {d['cantidad']} asiento(s)<br>"

            lbl = QLabel(texto)
            lbl.setAlignment(Qt.AlignLeft)
            lbl.setWordWrap(True)

            btn = QPushButton("Cerrar")
            btn.clicked.connect(dlg.close)

            layout.addWidget(lbl)
            layout.addWidget(btn)

            dlg.exec()
    # ---------------- DB helpers / loaders ----------------
    def load_all_trips_from_db(self):
        """
        Carga en memoria todos los viajes (futuros y pasados). Usado por Boletos.
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

    def load_conductores(self):
        try:
            cur = self.db.cursor(dictionary=True)
            cur.execute("""
                SELECT registro, conNombre, conPrimerApell, conSegundoApell
                FROM conductor
                ORDER BY conNombre, conPrimerApell, conSegundoApell
            """)
            rows = cur.fetchall()

            # mantener la primera opción "Todos"
            self.cmb_conductor.clear()
            self.cmb_conductor.addItem("Todos", None)
            for row in rows:
                fullname = " ".join(filter(None, [
                    row.get("conNombre", ""), row.get("conPrimerApell", ""), row.get("conSegundoApell", "")
                ])).strip()
                self.cmb_conductor.addItem(fullname, row.get("registro"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los conductores:\n{e}")
        finally:
            try:
                cur.close()
            except:
                pass

    def load_autobuses(self):
        try:
            cur = self.db.cursor(dictionary=True)
            cur.execute("SELECT numero, placas FROM autobus ORDER BY numero")
            rows = cur.fetchall()
            self.cmb_bus.clear()
            self.cmb_bus.addItem("Todos", None)
            for r in rows:
                display = f"{r.get('numero')} ({r.get('placas','')})"
                self.cmb_bus.addItem(display, r.get('numero'))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los autobuses:\n{e}")
        finally:
            try:
                cur.close()
            except:
                pass

    def load_ciudades(self):
        try:
            cur = self.db.cursor(dictionary=True)
            cur.execute("SELECT clave, nombre FROM ciudad ORDER BY nombre")
            rows = cur.fetchall()
            self.cmb_city.clear()
            self.cmb_city.addItem("Todas", None)
            for r in rows:
                self.cmb_city.addItem(r.get("nombre",""), r.get("clave"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las ciudades:\n{e}")
        finally:
            try:
                cur.close()
            except:
                pass

    # ---------------- filters and UI helpers ----------------
    def _on_scope_changed(self):
        idx = self.cmb_scope.currentIndex()
        self.date_edit.setVisible(idx == 0)
        self.cmb_month.setVisible(idx == 2)
        self.cmb_year.setVisible(idx == 2)

    def on_tipo_changed(self):
        self._update_filter_visibility()
        # reset apply flag? we keep behaviour consistent: apply_filters will use apply_pressed to determine date filtering
        self.apply_filters()

    def _update_filter_visibility(self):
        tipo = self.cmb_tipo.currentText()
        self.lbl_search_conductor.setVisible(False)
        self.cmb_conductor.setVisible(False)
        self.lbl_search_bus.setVisible(False)
        self.cmb_bus.setVisible(False)
        self.lbl_search_city.setVisible(False)
        self.cmb_city.setVisible(False)

        if tipo == "Conductor":
            self.lbl_search_conductor.setVisible(True)
            self.cmb_conductor.setVisible(True)
        elif tipo == "Autobús":
            self.lbl_search_bus.setVisible(True)
            self.cmb_bus.setVisible(True)
        elif tipo == "Ciudad":
            self.lbl_search_city.setVisible(True)
            self.cmb_city.setVisible(True)

    def on_apply_clicked(self):
        self.apply_pressed = True
        self.initial_load = False
        self.apply_filters()

    def apply_filters(self):
        tipo = self.cmb_tipo.currentText()
        # clear current table
        self._clear_table()
        if tipo == "Boletos":
            self._apply_kpi_boletos()
        elif tipo == "Conductor":
            self._apply_kpi_conductor()
        elif tipo == "Autobús":
            self._apply_kpi_autobus()
        elif tipo == "Ciudad":
            self._apply_kpi_ciudad()
        else:
            self.lbl_info.setText("Tipo desconocido.")

    # ---------------- KPI implementations (llenado de tabla) ----------------
    def _apply_kpi_boletos(self):
        # columnas: Viaje | Fecha salida | Origen | Destino | Autobús | Vendidos | Disponibles
        headers = ["Viaje", "Fecha salida", "Origen", "Destino", "Autobús", "Vendidos", "Disponibles"]
        self._setup_table_headers(headers)

        if self.initial_load:
            trips = self.all_trips[:]
        else:
            rng = self._compute_date_range()
            if rng is None:
                return
            start, end = rng
            trips = [
                t for t in self.all_trips
                if isinstance(t.get("departure"), datetime) and start <= t["departure"] <= end
            ]

        self.lbl_info.setText(f"Resultados: {len(trips)} viaje(s).")

        total_vendidos = 0
        total_disponibles = 0

        # poblar filas
        self.table.setRowCount(len(trips))
        for r, trip in enumerate(trips):
            try:
                stats = self._fetch_ticket_stats(trip.get("trip_id"), trip.get("seats_count") or 0)
            except Exception:
                stats = {"sold": 0, "available": trip.get("seats_count") or 0}
            total_vendidos += stats["sold"]
            total_disponibles += stats["available"]

            self._set_item(r, 0, str(trip.get("trip_id") or ""))
            self._set_item(r, 1, format_dt(trip.get("departure")))
            self._set_item(r, 2, str((trip.get("origin_city") or "").strip().title()))
            self._set_item(r, 3, str((trip.get("dest_city") or "").strip().title()))
            self._set_item(r, 4, str(trip.get("bus_number") or ""))
            self._set_item(r, 5, str(stats["sold"]))
            self._set_item(r, 6, str(stats["available"]))

        # ajustar columnas: estirar
        self._stretch_columns()
        # actualizar resumen
        self.lbl_info.setText(f"Resultados: {len(trips)} viaje(s).  |  Boletos vendidos: {total_vendidos}  |  Disponibles: {total_disponibles}")

    def _apply_kpi_conductor(self):
        # columnas: Conductor | Viaje | Salida | Llegada | Origen | Destino | Autobús | Matrícula
        headers = ["Conductor", "Viaje", "Salida", "Llegada", "Origen", "Destino", "Autobús"]
        self._setup_table_headers(headers)

        where_clauses = []
        params = []

        if self.apply_pressed:
            rng = self._compute_date_range()
            if rng is None:
                return
            start, end = rng
            where_clauses.append("v.fecHoraSalida BETWEEN %s AND %s")
            params.extend([start, end])

        conductor_id = self.cmb_conductor.currentData()
        if conductor_id is not None:
            where_clauses.append("v.conductor = %s")
            params.append(conductor_id)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        try:
            cur = self.db.cursor(dictionary=True)
            sql = f"""
                SELECT
                    v.numero AS trip_id,
                    v.fecHoraSalida AS departure,
                    v.fecHoraEntrada AS arrival,
                    corig.nombre AS origin_city,
                    cdest.nombre AS dest_city,
                    v.autobus AS bus_number,
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
            except:
                pass
            return
        finally:
            try:
                cur.close()
            except:
                pass

        if not rows:
            self.table.setRowCount(0)
            self.lbl_info.setText("Resultados: 0 viaje(s).")
            return

        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            fullname = " ".join(filter(None, [row.get("con_nombre") or "", row.get("con_ap1") or "", row.get("con_ap2") or ""])).strip()
            self._set_item(r, 0, fullname)
            self._set_item(r, 1, str(row.get("trip_id") or ""))
            self._set_item(r, 2, format_dt(row.get("departure")))
            self._set_item(r, 3, format_dt(row.get("arrival")))
            self._set_item(r, 4, str(row.get("origin_city") or ""))
            self._set_item(r, 5, str(row.get("dest_city") or ""))
            self._set_item(r, 6, str(row.get("bus_number") or ""))

        self._stretch_columns()
        self.lbl_info.setText(f"Resultados: {len(rows)} viaje(s).")

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.resizeColumnToContents(0)
        
    def _apply_kpi_autobus(self):
        # columnas: Número | Matrícula | Marca | Modelo | Año | Asientos
        headers = ["Número", "Matrícula", "Marca", "Modelo", "Año", "Asientos"]
        self._setup_table_headers(headers)

        where_clauses = []
        params = []

        if self.apply_pressed:
            rng = self._compute_date_range()
            if rng is None:
                return
            start, end = rng
            where_clauses.append("v.fecHoraSalida BETWEEN %s AND %s")
            params.extend([start, end])

        bus_id = self.cmb_bus.currentData()
        if bus_id is not None:
            where_clauses.append("v.autobus = %s")
            params.append(bus_id)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        try:
            cur = self.db.cursor(dictionary=True)
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
            except:
                pass
            return
        finally:
            try:
                cur.close()
            except:
                pass

        if not rows:
            self.table.setRowCount(0)
            self.lbl_info.setText("Resultados: 0 autobús(es).")
            return

        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            self._set_item(r, 0, str(row.get("bus_number") or ""))
            self._set_item(r, 1, str(row.get("placas") or ""))
            self._set_item(r, 2, str(row.get("marca_nombre") or ""))
            self._set_item(r, 3, str(row.get("modelo_nombre") or ""))
            self._set_item(r, 4, str(row.get("modelo_año") or ""))
            # Columna Asientos (con tooltip)
            asientos = str(row.get("numasientos") or "")
            item_asientos = QTableWidgetItem(asientos)
            item_asientos.setFlags(item_asientos.flags() & ~Qt.ItemIsEditable)

            # Tooltip mostrando “X asientos”
            item_asientos.setToolTip(f"Este autobús tiene {asientos} asientos")

            self.table.setItem(r, 5, item_asientos)

        self._stretch_columns()
        self.lbl_info.setText(f"Resultados: {len(rows)} autobús(es).")

        self.asientos_column_index = 5
        
    def _apply_kpi_ciudad(self):
        headers = ["Ciudad", "Salida", "Viaje", "Destino", "Autobús", "Matrícula", "Operador"]
        self._setup_table_headers(headers)

        where_clauses = []
        params = []

        # Aplicar filtro de fecha solo si el usuario presionó Aplicar (consistente con otras vistas)
        if self.apply_pressed:
            rng = self._compute_date_range()
            if rng is None:
                return
            start, end = rng
            where_clauses.append("v.fecHoraSalida BETWEEN %s AND %s")
            params.extend([start, end])

        # Filtro por ciudad (usamos currentData porque load_ciudades agrega clave como data)
        city_key = self.cmb_city.currentData()
        if city_key is not None:
            where_clauses.append("corig.clave = %s")
            params.append(city_key)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        try:
            cur = self.db.cursor(dictionary=True)
            sql = f"""
                SELECT
                    corig.nombre AS ciudad,
                    v.fecHoraSalida AS salida,
                    v.numero AS viaje,
                    cdest.nombre AS destino,
                    a.numero AS autobus,
                    a.placas AS matricula,
                    CONCAT(c.conNombre, ' ', c.conPrimerApell, ' ', c.conSegundoApell) AS operador
                FROM viaje v
                LEFT JOIN ruta r       ON v.ruta = r.codigo
                LEFT JOIN terminal tor ON r.origen = tor.numero
                LEFT JOIN terminal tde ON r.destino = tde.numero
                LEFT JOIN ciudad corig ON tor.ciudad = corig.clave
                LEFT JOIN ciudad cdest ON tde.ciudad = cdest.clave
                LEFT JOIN autobus a    ON v.autobus = a.numero
                LEFT JOIN conductor c  ON v.conductor = c.registro
                {where_sql}
                ORDER BY v.fecHoraSalida ASC
            """
            cur.execute(sql, tuple(params) if params else None)
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error cargando ciudades:\n{e}")
            try:
                cur.close()
            except:
                pass
            return
        finally:
            try:
                cur.close()
            except:
                pass

        # Poblar tabla
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            self._set_item(r, 0, row.get("ciudad", ""))
            self._set_item(r, 1, format_dt(row.get("salida")))
            self._set_item(r, 2, str(row.get("viaje") or ""))
            self._set_item(r, 3, row.get("destino", ""))
            self._set_item(r, 4, str(row.get("autobus") or ""))
            self._set_item(r, 5, row.get("matricula", ""))
            self._set_item(r, 6, row.get("operador", ""))

        # --- Ajustes de columnas (manteniendo tu layout para que no se corte)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)           # Ciudad
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents) # Salida
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) # Viaje
        header.setSectionResizeMode(3, QHeaderView.Stretch)           # Destino
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents) # Autobús
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents) # Matrícula
        header.setSectionResizeMode(6, QHeaderView.Stretch)           # Operador

        self.lbl_info.setText(f"Resultados: {len(rows)} viaje(s).")

    # ---------------- small helpers ----------------
    def _setup_table_headers(self, headers: List[str]):
        self.table.clear()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(0)
        # disable sorting (user requested NO sorting)
        self.table.setSortingEnabled(False)
        # header resize: stretch all columns
        for c in range(len(headers)):
            self.table.horizontalHeader().setSectionResizeMode(c, QHeaderView.Stretch)
        # small vertical header hidden
        self.table.verticalHeader().setVisible(False)
        # ensure no horizontal scroll
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def _set_item(self, row: int, col: int, text: str):
        item = QTableWidgetItem(text if text is not None else "")
        # make items non-editable
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(row, col, item)

    def _stretch_columns(self):
        # Ensure every column uses Stretch mode
        hdr = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            hdr.setSectionResizeMode(i, QHeaderView.Stretch)

    def _clear_table(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)

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
                # res may be tuple or dict
                if isinstance(res, (list, tuple)):
                    sold = int(res[0])
                elif isinstance(res, dict):
                    # fetch first value
                    sold = int(list(res.values())[0])
                else:
                    sold = int(res)
        except Exception as e:
            print("Error al obtener tickets:", e)
        finally:
            try:
                cur.close()
            except:
                pass

        available = seats_count - sold if seats_count and seats_count >= sold else max(0, (seats_count or 0) - sold)
        return {"sold": sold, "available": available}

    def _compute_date_range(self) -> Optional[Tuple[datetime, datetime]]:
        scope = self.cmb_scope.currentText()
        try:
            if scope == "Todos":
                return None 
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

    def reload_from_db(self):
        try:
            self.load_all_trips_from_db()
            self.load_conductores()
            self.load_autobuses()
            self.load_ciudades()
            self.apply_filters()
            QMessageBox.information(self, "Actualizado", f"Datos actualizados.\n{len(self.all_trips)} viajes cargados.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar:\n{e}")

    # ---------------- Export CSV ----------------
    def export_table_csv(self):
        if self.table.rowCount() == 0 or self.table.columnCount() == 0:
            QMessageBox.information(self, "Exportar CSV", "No hay datos para exportar.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Guardar CSV", f"kpi_export_{self.cmb_tipo.currentText().lower()}.csv", "CSV Files (*.csv)")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                # headers
                headers = [self.table.horizontalHeaderItem(c).text() if self.table.horizontalHeaderItem(c) else "" for c in range(self.table.columnCount())]
                f.write(",".join(headers) + "\n")
                for r in range(self.table.rowCount()):
                    vals = []
                    for c in range(self.table.columnCount()):
                        it = self.table.item(r, c)
                        vals.append(it.text() if it else "")
                    # escape commas by wrapping fields in quotes if needed
                    line = ",".join(['"{}"'.format(v.replace('"', '""')) if ("," in v or '"' in v or "\n" in v) else v for v in vals])
                    f.write(line + "\n")
            QMessageBox.information(self, "Exportado", "CSV exportado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar CSV:\n{e}")


# ----------------- Ejecución directa -----------------
def main():
    app = QApplication(sys.argv)
    win = KPIWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()