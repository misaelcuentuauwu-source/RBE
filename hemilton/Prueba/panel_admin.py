from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QStackedWidget, QFrame, QSizePolicy, QSpacerItem, QMessageBox,
    QScrollArea, QFormLayout, QDialog, QDialogButtonBox, QComboBox, QDateTimeEdit
)
from PySide6.QtCore import Qt, QDateTime
from gestionviajes import MainWindow
from PySide6.QtWidgets import QHeaderView
from conexion import crear_conexion
from viajes_programados import ProgramacionWindow
from PySide6.QtWidgets import QApplication
from kpi import KPIWindow
import kpi_calculos

## Modificar la info de un taquillero ##
def actualizar_taquillero_bd(registro, nombre, ap1, ap2, usuario, contrasena):
    try:
        cn = crear_conexion()
        cur = cn.cursor()
        cur.execute("""
            UPDATE taquillero
            SET taqNombre=%s, taqPrimerApell=%s, taqSegundoApell=%s,
                usuario=%s, contraseña=%s
            WHERE registro=%s
        """, (nombre, ap1, ap2, usuario, contrasena, registro))
        cn.commit()
        cur.close()
        cn.close()
        return True, None
    except Exception as e:
        return False, str(e)

## El dashboard ##

class PanelAdministrador(QMainWindow):
    def __init__(self, usuario_actual, volver_callback):
        super().__init__()
        self.usuario_actual = usuario_actual or {}
        self.volver_callback = volver_callback
        self.menu_collapsed = False

        # Colores
        COLOR_BG = "#f2f2f2"
        COLOR_PRIMARY = "#1181c3"
        COLOR_ACCENT = "#ed7237"
        COLOR_TEXT = "#222"

        self.setWindowTitle("Rutas Baja Express - Panel Administrador")
        self.resize(1200, 760)
        self.setMinimumSize(1000, 500)
        self.move(
            QApplication.primaryScreen().availableGeometry().center() - self.rect().center()
        )

        self.setStyleSheet(f"background:{COLOR_BG}; font-family: 'Segoe UI';")

        # permisos y tablas
        self.permisos = {
            "marca": ("A","A","A","A"),
            "conductor": ("A","A","A","A"),
            "ciudad": ("A","A","A","A"),
            "tipo_asiento": ("A","A","A","A"),
            "tipo_pasajero": ("A","A","A","A"),
            "tipo_pago": ("A","A","A","A"),
            "edo_viaje": ("A","A","A","A"),
            "pasajero": ("U,A","U,A","A","A"),
            "modelo": ("A","A","A","A"),
            "terminal": ("A","A","A","A"),
            "ruta": ("A","A","A","A"),
            "autobus": ("A","A","A","A"),
            "viaje": ("U,A","U,A","A","A"),
            "asiento": ("A","A","A","A"),
            "viaje_asiento": ("A","A","A","A"),
            "taquillero": ("A","A","A","A"),
            "pago": ("U,A","A","A","A"),
            "ticket": ("U,A","A","A","A"),
        }

        self.tablas = [
            "marca", "modelo", "autobus", "ciudad", "conductor", "ruta",
            "viaje", "asiento", "viaje_asiento", "taquillero", "tipo_pasajero",
            "tipo_pago", "edo_viaje", "ticket", "pasajero", "pago", "terminal"
        ]

        ## Layout ##
        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0,0,0,0)

        ## Scroolo pal sidebar ##
        sidebar_frame = QFrame()
        sidebar_frame.setStyleSheet(f"background:{COLOR_ACCENT};")
        sidebar_frame.setMinimumWidth(260)
        sidebar_frame.setMaximumWidth(320)
        sb_layout = QVBoxLayout(sidebar_frame)
        sb_layout.setContentsMargins(16,16,16,16)
        sb_layout.setSpacing(10)

        brand = QLabel("Rutas Baja Express")
        brand.setStyleSheet("color: white; font-size:22pt; font-weight:800;")
        sb_layout.addWidget(brand)

        ## Scroll par alos botones ##
        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setStyleSheet("background: transparent; border: none;")
        sa_widget = QWidget()
        sa_layout = QVBoxLayout(sa_widget)
        sa_layout.setContentsMargins(0,8,0,8)
        sa_layout.setSpacing(8)

        ## Style ##
        def make_nav(text):
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setFixedHeight(44)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: white;
                    color: {COLOR_ACCENT};
                    border-radius: 10px;
                    padding-left: 14px;
                    text-align: left;
                    font-weight:700;
                }}
                QPushButton:hover {{ background: #fff5e6; }}
            """)
            return btn

        self.btn_dashboard = make_nav("KPI'S")
        sa_layout.addWidget(self.btn_dashboard)

        self.btn_salidas = make_nav("Salidas")
        sa_layout.addWidget(self.btn_salidas)

        # Boton para agregar viajes ##
        self.btn_agregar_viaje = make_nav("Agregar Viaje")
        sa_layout.addWidget(self.btn_agregar_viaje)

        self.btn_historial = make_nav("Historial de Viajes")
        sa_layout.addWidget(self.btn_historial)

        self.btn_gestion = make_nav("Gestión ▾")
        sa_layout.addWidget(self.btn_gestion)

        ## Contenedor ##
        self.gestion_container = QWidget()
        gc_layout = QVBoxLayout(self.gestion_container)
        gc_layout.setContentsMargins(6,6,6,6)
        gc_layout.setSpacing(6)
        self.tab_buttons = {}
        for t in self.tablas:
            b = QPushButton(t.capitalize())
            b.setCursor(Qt.PointingHandCursor)
            b.setFixedHeight(36)
            b.setStyleSheet("""
                QPushButton {
                    background: white;
                    color: #ff8c00;
                    border-radius: 8px;
                    padding-left:10px;
                    text-align:left;
                }
                QPushButton:hover { background:#fff7e0; color:#c96f00; }
            """)
            b.clicked.connect(lambda checked=False, tt=t: self.on_tab_selected(tt))
            gc_layout.addWidget(b)
            self.tab_buttons[t] = b
        self.gestion_container.setVisible(False)
        sa_layout.addWidget(self.gestion_container)

        ## Scroll final ##
        sa_layout.addSpacerItem(QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding))
        sa_widget.setLayout(sa_layout)
        sa.setWidget(sa_widget)
        sb_layout.addWidget(sa)

        ## Configuración de contenedor ##
        config_container = QFrame()
        config_container.setStyleSheet("background: transparent;")
        config_layout = QVBoxLayout(config_container)
        config_layout.setContentsMargins(0, 8, 0, 8)

        self.btn_config = make_nav("Configuración")
        self.btn_config.setStyleSheet(f"""
            QPushButton {{
                background: white;
                color: {COLOR_ACCENT};
                border-radius: 10px;
                padding-left: 14px;
                text-align: left;
                font-weight:700;
            }}
            QPushButton:hover {{ background: #fff5e6; color: #c96f00; }}
        """)
        config_layout.addWidget(self.btn_config)


        sb_layout.addSpacerItem(QSpacerItem(10,10,QSizePolicy.Minimum,QSizePolicy.Expanding))

        self.btn_logout = QPushButton("Cerrar sesión")
        self.btn_logout.setCursor(Qt.PointingHandCursor)
        self.btn_logout.setFixedHeight(44)
        self.btn_logout.setStyleSheet(f"""
            QPushButton {{ background:{COLOR_PRIMARY}; color:#111; border-radius:10px; font-weight:800; }}
            QPushButton:hover {{ background:#e6de00; }}
        """)
        sb_layout.addWidget(config_container)
        sb_layout.addWidget(self.btn_logout)

        ## Area del contenedor ##
        content_frame = QFrame()
        content_ly = QVBoxLayout(content_frame)
        content_ly.setContentsMargins(14,14,14,14)

        top = QHBoxLayout()
        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setFixedSize(40,40)
        self.toggle_btn.setStyleSheet(f"background:{COLOR_PRIMARY}; border-radius:8px; font-weight:900;")
        top.addWidget(self.toggle_btn)
        top.addStretch()
        name = f"{self.usuario_actual.get('taqNombre','')} {self.usuario_actual.get('taqPrimerApell','')}"
        self.lbl_user = QLabel(f"Hola, {name}")
        self.lbl_user.setStyleSheet(f"color:{COLOR_TEXT}; font-weight:600;")
        top.addWidget(self.lbl_user)
        content_ly.addLayout(top)

        ## El stacked ##
        self.stacked = QStackedWidget()
        ## Primera pagina ##
        self.page_inicio = QWidget()
        inicio_layout = QVBoxLayout(self.page_inicio)

        titulo_inicio = QLabel("Salidas")
        titulo_inicio.setStyleSheet("font-size:26pt; font-weight:800; color:#1181c3;")
        inicio_layout.addWidget(titulo_inicio)

        ## widget integrado ##
        self.viajes_programados_widget = ProgramacionWindow()
        self.viajes_programados_widget.setWindowFlags(Qt.Widget)
        inicio_layout.addWidget(self.viajes_programados_widget)

        self.stacked.addWidget(self.page_inicio)
        self.stacked.setCurrentWidget(self.page_inicio)

        ## Dashboard ##
        self.page_dashboard = QWidget()
        dash_layout = QVBoxLayout(self.page_dashboard)
        hdr = QLabel("Dashboard — Administrador")
        hdr.setStyleSheet(f"font-size:26pt; font-weight:800; color:{COLOR_PRIMARY};")
        dash_layout.addWidget(hdr)
        dash_layout.addSpacing(8)

        self.placeholder_frame = QFrame()
        self.placeholder_frame.setStyleSheet("background:white; border-radius:12px; padding:18px;")
        ph_ly = QVBoxLayout(self.placeholder_frame)
        ph_lbl = QLabel("Selecciona una opción del menú para comenzar.")
        ph_lbl.setAlignment(Qt.AlignCenter)
        ph_ly.addWidget(ph_lbl)
        dash_layout.addWidget(self.placeholder_frame)


        self.dashboard_body = QVBoxLayout()
        dash_layout.addLayout(self.dashboard_body)

        self.stacked.addWidget(self.page_dashboard)

        ## Historial de viajes ##
        self.page_historial = QWidget()
        self.historial_layout = QVBoxLayout(self.page_historial)

        ## instancia ##
        self.historial_widget = MainWindow()
        self.historial_layout.addWidget(self.historial_widget)

        self.stacked.addWidget(self.page_historial)

        ## KPIS ##
        self.page_kpis = QWidget()
        kpi_layout = QVBoxLayout(self.page_kpis)
        kpi_layout.setContentsMargins(0, 0, 0, 0)
        kpi_layout.setSpacing(10)

        ## Stacked interno para cambiar de KPIS##
        self.kpi_stacked = QStackedWidget()

        ## Datos especificos ##
        self.kpi_datos_especificos = KPIWindow()
        self.kpi_datos_especificos.setWindowFlags(Qt.Widget)
        self.kpi_stacked.addWidget(self.kpi_datos_especificos)

        ## Datos generales ##
        self.kpi_datos_generales = kpi_calculos.KPIWindowGenerales()
        self.kpi_datos_generales.setWindowFlags(Qt.Widget)
        self.kpi_stacked.addWidget(self.kpi_datos_generales)

        ## Botones ##
        switch_layout = QHBoxLayout()
        switch_layout.setAlignment(Qt.AlignCenter)

        self.btn_especificos = QPushButton("Datos Específicos")
        self.btn_generales = QPushButton("Datos Generales")

        switch_layout.addWidget(self.btn_especificos)
        switch_layout.addWidget(self.btn_generales)

        self.btn_especificos.clicked.connect(lambda: self.kpi_stacked.setCurrentIndex(0))
        self.btn_generales.clicked.connect(lambda: self.kpi_stacked.setCurrentIndex(1))

        kpi_layout.addWidget(self.kpi_stacked)
        kpi_layout.addLayout(switch_layout)

        self.stacked.addWidget(self.page_kpis)

        ## Pagina de configuracion ##
        self.page_config = QWidget()
        cfg_ly = QVBoxLayout(self.page_config)
        cfg_ly.setContentsMargins(18,18,18,18)
        cfg_title = QLabel("Configuración de Usuario")
        cfg_title.setStyleSheet(f"font-size:18pt; font-weight:800; color:{COLOR_PRIMARY};")
        cfg_ly.addWidget(cfg_title)

        cfg_ly.addWidget(QLabel("Nombre:"))
        self.cfg_nombre = QLineEdit(self.usuario_actual.get('taqNombre',''))
        cfg_ly.addWidget(self.cfg_nombre)
        cfg_ly.addWidget(QLabel("Primer Apellido:"))
        self.cfg_ap1 = QLineEdit(self.usuario_actual.get('taqPrimerApell',''))
        cfg_ly.addWidget(self.cfg_ap1)
        cfg_ly.addWidget(QLabel("Segundo Apellido:"))
        self.cfg_ap2 = QLineEdit(self.usuario_actual.get('taqSegundoApell',''))
        cfg_ly.addWidget(self.cfg_ap2)
        cfg_ly.addWidget(QLabel("Usuario:"))
        self.cfg_user = QLineEdit(self.usuario_actual.get('usuario',''))
        cfg_ly.addWidget(self.cfg_user)
        cfg_ly.addWidget(QLabel("Contraseña:"))
        self.cfg_pass = QLineEdit(self.usuario_actual.get('contraseña',''))
        self.cfg_pass.setEchoMode(QLineEdit.Password)
        cfg_ly.addWidget(self.cfg_pass)

        btn_save = QPushButton("Guardar cambios")
        btn_save.setFixedHeight(40)
        btn_save.setStyleSheet(f"background:{COLOR_PRIMARY}; border-radius:8px; font-weight:800;")
        cfg_ly.addWidget(btn_save)

        ## Boton para regresar ##
        btn_back = QPushButton("Volver al Dashboard")
        btn_back.setFixedHeight(36)
        btn_back.setStyleSheet("background:#ffffff; border-radius:8px; font-weight:700; color:#ff8c00;")
        cfg_ly.addWidget(btn_back)

        self.stacked.addWidget(self.page_config)

        ## Añadir contenedor ##
        content_ly.addWidget(self.stacked)
        root_layout.addWidget(sidebar_frame)
        root_layout.addWidget(content_frame)
        self.setCentralWidget(root)

        # Conexion de los botones ##
        self.toggle_btn.clicked.connect(self.toggle_menu)
        self.btn_gestion.clicked.connect(self._toggle_gestion)
        self.btn_dashboard.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page_kpis))
        self.btn_historial.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page_historial))
        self.btn_config.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page_config))
        btn_back.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page_dashboard))
        self.btn_logout.clicked.connect(self.cerrar_sesion)
        btn_save.clicked.connect(self._guardar_config)
        self.btn_salidas.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page_inicio))
        self.btn_agregar_viaje.clicked.connect(self.open_add_trip_dialog)  # Conexión del nuevo botón


        self.show()

    # Método para registrar viaje ##
    def open_add_trip_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Agregar Nuevo Viaje")
        dlg.setMinimumWidth(500)

        layout = QFormLayout(dlg)

        ## Campos para llenar ##
        self.departure_edit = QDateTimeEdit()
        self.departure_edit.setDateTime(QDateTime.currentDateTime().addDays(1))
        self.departure_edit.setCalendarPopup(True)
        self.departure_edit.setDisplayFormat("yyyy-MM-dd HH:mm")

        self.arrival_edit = QDateTimeEdit()
        self.arrival_edit.setDateTime(QDateTime.currentDateTime().addDays(1).addSecs(3600))  # 1 hora después
        self.arrival_edit.setCalendarPopup(True)
        self.arrival_edit.setDisplayFormat("yyyy-MM-dd HH:mm")

        self.route_combo = QComboBox()
        self.bus_combo = QComboBox()
        self.driver_combo = QComboBox()
        self.status_combo = QComboBox()

        ## Cargar datos para los combos ##
        self.load_combo_data()

        layout.addRow("Fecha y Hora de Salida:", self.departure_edit)
        layout.addRow("Fecha y Hora de Llegada:", self.arrival_edit)
        layout.addRow("Ruta:", self.route_combo)
        layout.addRow("Autobús:", self.bus_combo)
        layout.addRow("Conductor:", self.driver_combo)
        layout.addRow("Estado:", self.status_combo)

        ## Botones ##
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.add_trip(dlg))
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)

        dlg.exec()

    def load_combo_data(self):
        try:
            cn = crear_conexion()
            cur = cn.cursor(dictionary=True)

            ## Cargar rutas ##
            cur.execute("""
                SELECT r.codigo, CONCAT(c1.nombre, ' → ', c2.nombre) AS ruta_desc
                FROM ruta r
                JOIN terminal t1 ON r.origen = t1.numero
                JOIN terminal t2 ON r.destino = t2.numero
                JOIN ciudad c1 ON t1.ciudad = c1.clave
                JOIN ciudad c2 ON t2.ciudad = c2.clave
            """)
            for row in cur.fetchall():
                self.route_combo.addItem(f"Ruta #{row['codigo']} ({row['ruta_desc']})", row['codigo'])

            ## Cargar autobuses ##
            cur.execute("SELECT numero, placas FROM autobus")
            for row in cur.fetchall():
                self.bus_combo.addItem(f"Autobús #{row['numero']} ({row['placas']})", row['numero'])

            ## Cargar conductores ##
            cur.execute("SELECT registro, CONCAT(conNombre, ' ', conPrimerApell) AS nombre FROM conductor")
            for row in cur.fetchall():
                self.driver_combo.addItem(f"Conductor #{row['registro']} ({row['nombre']})", row['registro'])

            ## Cargar estados de viaje ##
            cur.execute("SELECT numero, nombre FROM edo_viaje")
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

            ## Insertar el viaje ##
            cur.execute("""
                INSERT INTO viaje (fecHoraSalida, fecHoraEntrada, ruta, estado, autobus, conductor)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (departure, arrival, route, status, bus, driver))

            ## Obtener el ID ##
            trip_id = cur.lastrowid

            ## Crear los registros en viaje_asiento ##
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

            QMessageBox.information(self, "Éxito", "Viaje agregado correctamente.")
            dialog.accept()

            ## Recargar los viajes en la página de salidas ##
            if hasattr(self, 'viajes_programados_widget'):
                self.viajes_programados_widget.reload_from_db()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar el viaje: {e}")
    def toggle_menu(self):
        if self.menu_collapsed:
            self.centralWidget().layout().itemAt(0).widget().setFixedWidth(300)
            self.menu_collapsed = False
        else:
            self.centralWidget().layout().itemAt(0).widget().setFixedWidth(64)
            self.menu_collapsed = True

    def _toggle_gestion(self):
        visible = self.gestion_container.isVisible()
        self.gestion_container.setVisible(not visible)
        self.btn_gestion.setText("Gestión ▾" if visible else "Gestión ▴")

    def on_tab_selected(self, tabla):
        self.stacked.setCurrentWidget(self.page_dashboard)
        self.mostrar_gestion_tabla(tabla)


    def _set_placeholder_impl(self, layout_target, text):
        placeholder = QFrame()
        placeholder.setStyleSheet("background:white; border-radius:12px; padding:16px;")
        ly = QVBoxLayout(placeholder)
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignCenter)
        ly.addWidget(lbl)
        layout_target.addWidget(placeholder)

    def _clear_layout(self, layout):
        while layout.count():
            it = layout.takeAt(0)
            w = it.widget()
            if w:
                w.deleteLater()

    def mostrar_gestion_tabla(self, tabla):
        self._clear_layout(self.dashboard_body)

        title = QLabel(f"Gestión — {tabla}")
        title.setStyleSheet("font-size:20pt; font-weight:800; color:#ff8c00;")
        self.dashboard_body.addWidget(title)

        permisos = self.permisos.get(tabla, ("A","A","A","A"))
        row_actions = QHBoxLayout()
        ## Insert ##
        if "A" in permisos[0] or "U" in permisos[0]:
            b_ins = QPushButton("Insertar")
            b_ins.setFixedHeight(36)
            b_ins.setStyleSheet("background:#52b788;color:white;border-radius:8px;font-weight:800;")
            b_ins.clicked.connect(lambda checked=False, t=tabla: self.accion_insertar(t))
            row_actions.addWidget(b_ins)
        ## Leer ##
        if "A" in permisos[3] or "U" in permisos[3]:
            b_leer = QPushButton("Leer")
            b_leer.setFixedHeight(36)
            b_leer.setStyleSheet("background:#457b9d;color:white;border-radius:8px;font-weight:800;")
            b_leer.clicked.connect(lambda checked=False, t=tabla: self.accion_leer(t))
            row_actions.addWidget(b_leer)
        row_actions.addStretch()
        self.dashboard_body.addLayout(row_actions)

        ## Contenedor ##
        self.current_area = QVBoxLayout()
        self.current_area.setContentsMargins(0,12,0,0)
        self.dashboard_body.addLayout(self.current_area)

        if "A" in permisos[3] or "U" in permisos[3]:
            self.accion_leer(tabla)

    def _describe_table(self, tabla):
        try:
            cn = crear_conexion()
            try:
                cur = cn.cursor(dictionary=True)
            except TypeError:
                cur = cn.cursor()
            cur.execute(f"SHOW COLUMNS FROM `{tabla}`")
            cols = cur.fetchall()
            if cols and len(cols)>0 and not isinstance(cols[0], dict):
                cols = [dict(zip([d[0] for d in cur.description], r)) for r in cols]
            cur.close()
            cn.close()
            return cols
        except Exception as e:
            print("DESCRIBE ERROR:", e)
            return None

    def _get_primary_key_value(self, tabla, row):
        cols = self._describe_table(tabla)
        pk = None
        for c in (cols or []):
            if c.get("Key") == "PRI":
                pk = c["Field"]
                break
        if not pk:
            pk = list(row.keys())[0]
        return pk, row.get(pk)

    def _fk_map_for_table(self, tabla):
        fk = {}
        try:
            cn = crear_conexion()
            cur = cn.cursor()
            cur.execute("""
                SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND REFERENCED_TABLE_NAME IS NOT NULL
            """, (tabla,))
            rows = cur.fetchall()
            cur.close()
            cn.close()
            for r in rows:
                if isinstance(r, dict):
                    col = r["COLUMN_NAME"]; rt = r["REFERENCED_TABLE_NAME"]; rc = r["REFERENCED_COLUMN_NAME"]
                else:
                    col, rt, rc = r[0], r[1], r[2]
                fk[col] = (rt, rc)
        except Exception:
            pass
        return fk

    def _pick_display_column(self, table):
        cols = self._describe_table(table)
        if not cols:
            return None
        names = [c["Field"].lower() for c in cols]
        for pref in ("nombre","name","titulo","descripcion","nom","label"):
            if pref in names:
                return cols[names.index(pref)]["Field"]
        for c in cols:
            t = c["Type"].lower()
            if "char" in t or "varchar" in t or "text" in t:
                return c["Field"]
        return cols[0]["Field"]

    ## Leer cartas ##
    def accion_leer(self, tabla):
        if not hasattr(self, "current_area") or self.current_area is None:
            self.current_area = QVBoxLayout()
            self.dashboard_body.addLayout(self.current_area)
        self._clear_layout(self.current_area)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        vlay = QVBoxLayout(container)
        vlay.setSpacing(12)
        vlay.setContentsMargins(8,8,8,8)

        try:
            cn = crear_conexion()
            try:
                cur = cn.cursor(dictionary=True)
            except TypeError:
                cur = cn.cursor()
            cur.execute(f"SELECT * FROM `{tabla}` LIMIT 500")
            rows = cur.fetchall()
            if rows and len(rows)>0 and not isinstance(rows[0], dict):
                cols = [d[0] for d in cur.description]
                rows = [dict(zip(cols, r)) for r in rows]
            cur.close()
            cn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"No se pudo leer {tabla}: {e}")
            return

        if not rows:
            empty = QFrame()
            empty.setStyleSheet("background:white; border-radius:10px; padding:12px;")
            ly = QVBoxLayout(empty)
            ly.addWidget(QLabel("No hay registros."))
            vlay.addWidget(empty)
        else:
            for row in rows:
                card = QFrame()
                card.setStyleSheet("background:white; border-radius:10px; padding:12px;")
                hl = QHBoxLayout(card)

                left = QVBoxLayout()
                left.setSpacing(4)
                for i, (k, val) in enumerate(row.items()):
                    lbl = QLabel(f"<b>{k}</b>: {val}")
                    lbl.setStyleSheet("font-size:11pt; color:#333;")
                    left.addWidget(lbl)
                    if i >= 5:
                        break
                hl.addLayout(left)

                right = QVBoxLayout()
                right.addStretch()
                pk_name, pk_val = self._get_primary_key_value(tabla, row)
                perms = self.permisos.get(tabla, ("A","A","A","A"))

                if "A" in perms[1] or "U" in perms[1]:
                    btn_edit = QPushButton("Editar")
                    btn_edit.setFixedWidth(90)
                    btn_edit.setStyleSheet("background:#ffb703;color:white;border-radius:6px;padding:6px;")
                    btn_edit.clicked.connect(lambda checked=False, t=tabla, k=pk_name, v=pk_val: self._abrir_form_modificar(t,k,v))
                    right.addWidget(btn_edit)

                if "A" in perms[2] or "U" in perms[2]:
                    btn_del = QPushButton("Eliminar")
                    btn_del.setFixedWidth(90)
                    btn_del.setStyleSheet("background:#e63946;color:white;border-radius:6px;padding:6px;")
                    btn_del.clicked.connect(lambda checked=False, t=tabla, k=pk_name, v=pk_val: self._eliminar_registro(t,k,v))
                    right.addWidget(btn_del)

                btn_view = QPushButton("Ver")
                btn_view.setFixedWidth(90)
                btn_view.setStyleSheet("background:#6c757d;color:white;border-radius:6px;padding:6px;")
                copied_row = dict(row)
                btn_view.clicked.connect(lambda checked=False, t=tabla, r=copied_row: self._modal_leer(t,r))
                right.addWidget(btn_view)

                right.addStretch()
                hl.addLayout(right)
                vlay.addWidget(card)

        scroll.setWidget(container)
        self.current_area.addWidget(scroll)

    def accion_insertar(self, tabla):
        cols = self._describe_table(tabla)
        if not cols:
            QMessageBox.critical(self, "Error", "No se pudo obtener esquema.")
            return
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Insertar en {tabla}")
        form = QFormLayout()
        widgets = {}
        fk_map = self._fk_map_for_table(tabla)
        for c in cols:
            name = c["Field"]
            if c.get("Extra","").lower() == "auto_increment":
                continue
            if name in fk_map:
                ref_table, ref_col = fk_map[name]
                combo = QComboBox()
                combo.addItem("— seleccionar —", None)
                try:
                    cn = crear_conexion()
                    try:
                        cur = cn.cursor(dictionary=True)
                    except TypeError:
                        cur = cn.cursor()
                    disp = self._pick_display_column(ref_table)
                    cur.execute(f"SELECT `{ref_col}`, `{disp}` FROM `{ref_table}` LIMIT 1000")
                    rows = cur.fetchall()
                    if rows and not isinstance(rows[0], dict):
                        cols_tmp = [d[0] for d in cur.description]
                        rows = [dict(zip(cols_tmp, r)) for r in rows]
                    for r in rows:
                        combo.addItem(str(r.get(disp) or r.get(ref_col)), r.get(ref_col))
                    cur.close()
                    cn.close()
                except Exception:
                    combo.addItem("[error cargar]", None)
                form.addRow(QLabel(name+":"), combo)
                widgets[name] = combo
            else:
                w = QLineEdit()
                if "date" in c["Type"] or "datetime" in c["Type"]:
                    w.setPlaceholderText("YYYY-MM-DD or YYYY-MM-DD HH:MM:SS")
                form.addRow(QLabel(name+":"), w)
                widgets[name] = w
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        form.addWidget(buttons)
        dlg.setLayout(form)

        if dlg.exec() == QDialog.Accepted:
            fields = []
            vals = []
            for k, widget in widgets.items():
                if isinstance(widget, QComboBox):
                    v = widget.currentData()
                else:
                    v = widget.text().strip()
                if v == "":
                    v = None
                fields.append(f"`{k}`")
                vals.append(v)
            try:
                cn = crear_conexion()
                cur = cn.cursor()
                sql = f"INSERT INTO `{tabla}` ({', '.join(fields)}) VALUES ({', '.join(['%s']*len(vals))})"
                cur.execute(sql, tuple(vals))
                cn.commit()
                cur.close()
                cn.close()
                QMessageBox.information(self, "OK", "Registro insertado.")
                self.accion_leer(tabla)
            except Exception as e:
                QMessageBox.critical(self, "Error BD", f"No se pudo insertar: {e}")

    def _abrir_form_modificar(self, tabla, pk_name, pk_value):
        cols = self._describe_table(tabla)
        if not cols:
            QMessageBox.critical(self, "Error", "No se pudo obtener esquema.")
            return
        try:
            cn = crear_conexion()
            try:
                cur = cn.cursor(dictionary=True)
            except TypeError:
                cur = cn.cursor()
            cur.execute(f"SELECT * FROM `{tabla}` WHERE `{pk_name}` = %s", (pk_value,))
            row = cur.fetchone()
            if row and not isinstance(row, dict):
                row = dict(zip([d[0] for d in cur.description], row))
            cur.close()
            cn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"No se pudo leer registro: {e}")
            return
        if not row:
            QMessageBox.warning(self, "No encontrado", "Registro no existe")
            return

        dlg = QDialog(self)
        dlg.setWindowTitle(f"Editar — {tabla} : {pk_value}")
        form = QFormLayout()
        widgets = {}
        fk_map = self._fk_map_for_table(tabla)
        for c in cols:
            name = c["Field"]
            val = row.get(name)
            if c.get("Key") == "PRI":
                w = QLineEdit("" if val is None else str(val))
                w.setReadOnly(True)
                form.addRow(QLabel(name+":"), w)
                widgets[name] = w
                continue
            if name in fk_map:
                ref_table, ref_col = fk_map[name]
                combo = QComboBox()
                combo.addItem("— seleccionar —", None)
                try:
                    cn = crear_conexion()
                    try:
                        cur = cn.cursor(dictionary=True)
                    except TypeError:
                        cur = cn.cursor()
                    disp = self._pick_display_column(ref_table)
                    cur.execute(f"SELECT `{ref_col}`, `{disp}` FROM `{ref_table}` LIMIT 1000")
                    rows = cur.fetchall()
                    if rows and not isinstance(rows[0], dict):
                        cols_tmp = [d[0] for d in cur.description]
                        rows = [dict(zip(cols_tmp, r)) for r in rows]
                    for r in rows:
                        combo.addItem(str(r.get(disp) or r.get(ref_col)), r.get(ref_col))
                    cur.close()
                    cn.close()
                except Exception:
                    pass
                idx = combo.findData(val)
                if idx >= 0:
                    combo.setCurrentIndex(idx)
                form.addRow(QLabel(name+":"), combo)
                widgets[name] = combo
            else:
                w = QLineEdit("" if val is None else str(val))
                form.addRow(QLabel(name+":"), w)
                widgets[name] = w

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        form.addWidget(buttons)
        dlg.setLayout(form)

        if dlg.exec() == QDialog.Accepted:
            setters = []
            vals = []
            for name, widget in widgets.items():
                if name == pk_name:
                    continue
                if isinstance(widget, QComboBox):
                    v = widget.currentData()
                else:
                    v = widget.text().strip()
                if v == "":
                    v = None
                setters.append(f"`{name}` = %s")
                vals.append(v)
            vals.append(pk_value)
            sql = f"UPDATE `{tabla}` SET {', '.join(setters)} WHERE `{pk_name}` = %s"
            try:
                cn = crear_conexion()
                cur = cn.cursor()
                cur.execute(sql, tuple(vals))
                cn.commit()
                cur.close()
                cn.close()
                QMessageBox.information(self, "OK", "Registro actualizado")
                self.accion_leer(tabla)
            except Exception as e:
                QMessageBox.critical(self, "Error BD", f"No se pudo actualizar: {e}")

    def _eliminar_registro(self, tabla, pk_name, pk_value):
        if QMessageBox.question(self, "Confirmar", f"Eliminar registro {pk_value} de {tabla}?", QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
            return
        try:
            cn = crear_conexion()
            cur = cn.cursor()
            cur.execute(f"DELETE FROM `{tabla}` WHERE `{pk_name}` = %s", (pk_value,))
            cn.commit()
            cur.close()
            cn.close()
            QMessageBox.information(self, "OK", "Registro eliminado")
            self.accion_leer(tabla)
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"No se pudo eliminar: {e}")

    def _modal_leer(self, tabla, row):
        dlg = QDialog(self)
        dlg.setWindowTitle(f"{tabla} — Detalle")
        dlg.setModal(True)
        dlg.setMinimumWidth(520)
        main = QVBoxLayout(dlg)
        title = QLabel(f"Detalles — {tabla}")
        title.setStyleSheet("font-size:16pt; font-weight:700; color:#ff8c00;")
        main.addWidget(title)
        form = QFormLayout()
        for k, v in row.items():
            key_lbl = QLabel(f"{k}:")
            key_lbl.setStyleSheet("font-weight:700; color:#333;")
            val_lbl = QLabel(str(v))
            val_lbl.setStyleSheet("color:#444;")
            form.addRow(key_lbl, val_lbl)
        main.addLayout(form)
        btn_close = QPushButton("Cerrar")
        btn_close.setStyleSheet("background:#6c757d;color:white;padding:8px;border-radius:6px;")
        btn_close.clicked.connect(dlg.accept)
        main.addWidget(btn_close, alignment=Qt.AlignRight)
        dlg.exec()

    def _guardar_config(self):
        nombre = self.cfg_nombre.text().strip()
        ap1 = self.cfg_ap1.text().strip()
        ap2 = self.cfg_ap2.text().strip()
        usuario = self.cfg_user.text().strip()
        contrasena = self.cfg_pass.text().strip()
        if not (nombre and ap1 and usuario and contrasena):
            QMessageBox.warning(self, "Atención", "Campos obligatorios incompletos")
            return
        ok, err = actualizar_taquillero_bd(self.usuario_actual.get('registro'), nombre, ap1, ap2, usuario, contrasena)
        if ok:
            QMessageBox.information(self, "Éxito", "Datos actualizados correctamente")
            self.usuario_actual.update({
                'taqNombre': nombre, 'taqPrimerApell': ap1, 'taqSegundoApell': ap2, 'usuario': usuario, 'contraseña': contrasena
            })
            self.lbl_user.setText(f"Hola, {nombre} {ap1}")
            self.stacked.setCurrentWidget(self.page_dashboard)
        else:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar: {err}")

    def cerrar_sesion(self):
        if QMessageBox.question(self, "Confirmar", "¿Cerrar sesión?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.close()
            try:
                self.volver_callback()
            except Exception:
                pass