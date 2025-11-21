# panel_admin.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QStackedWidget, QFrame, QSizePolicy, QSpacerItem, QMessageBox
)
from PySide6.QtCore import Qt
from conexion import crear_conexion

# Función para actualizar taquillero (igual que PanelPrincipal)
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

# ===============================
# Panel Administrador
# ===============================
class PanelAdministrador(QMainWindow):
    def __init__(self, usuario_actual, volver_callback):
        super().__init__()
        self.usuario_actual = usuario_actual or {}
        self.volver_callback = volver_callback
        self.menu_colapsado = False

        # Colores corporativos
        COLOR_FONDO = "#f2f2f2"
        COLOR_PRINCIPAL = "#f2e800"   # Amarillo limón
        COLOR_NARANJA = "#ff8c00"     # Naranja fuerte
        COLOR_TEXTO = "#2b2b2b"

        self.setWindowTitle("Rutas Baja Express - Panel Administrador")
        self.setGeometry(100, 100, 1000, 640)
        self.setStyleSheet(f"background-color: {COLOR_FONDO}; font-family: 'Segoe UI';")

        # ========================= CONTENEDOR PRINCIPAL =========================
        central = QWidget()
        layout_main = QHBoxLayout(central)

        # ========================= SIDEBAR =========================
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(260)
        self.sidebar.setStyleSheet(f"background-color: {COLOR_NARANJA};")
        layout_sidebar = QVBoxLayout(self.sidebar)

        self.brand = QLabel("Rutas Baja Express")
        self.brand.setStyleSheet("color: white; font-size: 16pt; font-weight: bold; padding: 16px;")
        layout_sidebar.addWidget(self.brand)

        # Botón de navegación
        def nav_button(text):
            btn = QPushButton(text)
            btn.setObjectName("btn_nav")
            btn.setStyleSheet(f"""
                QPushButton#btn_nav {{
                    background-color: white;
                    color: {COLOR_NARANJA};
                    border: none;
                    text-align: left;
                    padding: 10px 18px;
                    font-size: 11pt;
                    border-radius: 6px;
                    margin: 4px 12px;
                }}
                QPushButton#btn_nav:hover {{
                    background-color: #fff9e5;
                    color: {COLOR_PRINCIPAL};
                }}
            """)
            return btn

        # Botones del menú admin
        self.btn_taquilleros = nav_button("Gestión de Taquilleros")
        self.btn_terminales = nav_button("Terminales")
        self.btn_viajes = nav_button("Gestión de Viajes")
        self.btn_reportes = nav_button("Reportes")
        self.btn_config = nav_button("Configuración")

        layout_sidebar.addWidget(self.btn_taquilleros)
        layout_sidebar.addWidget(self.btn_terminales)
        layout_sidebar.addWidget(self.btn_viajes)
        layout_sidebar.addWidget(self.btn_reportes)
        layout_sidebar.addWidget(self.btn_config)
        layout_sidebar.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botón cerrar sesión
        self.btn_logout = QPushButton("Cerrar sesión")
        self.btn_logout.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRINCIPAL};
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                margin: 12px;
            }}
            QPushButton:hover {{
                background-color: #d6d600;
            }}
        """)
        layout_sidebar.addWidget(self.btn_logout)

        # ========================= ÁREA DE CONTENIDO =========================
        main_content = QFrame()
        layout_content = QVBoxLayout(main_content)

        # Topbar
        topbar = QFrame()
        topbar.setMaximumHeight(70)
        layout_topbar = QHBoxLayout(topbar)

        self.btn_toggle = QPushButton("☰")
        self.btn_toggle.setFixedSize(36, 36)
        self.btn_toggle.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRINCIPAL};
                color: white;
                border-radius: 8px;
                font-size: 14pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #d6d600;
            }}
        """)
        layout_topbar.addWidget(self.btn_toggle)
        layout_topbar.addStretch()

        # Texto de bienvenida
        taq_nombre = self.usuario_actual.get('taqNombre','')
        taq_primer = self.usuario_actual.get('taqPrimerApell','')
        taq_seg = self.usuario_actual.get('taqSegundoApell','')
        self.welcome = QLabel(f"Hola, {taq_nombre} {taq_primer} {taq_seg}")
        self.welcome.setStyleSheet(f"font-size: 11pt; color: {COLOR_TEXTO};")
        layout_topbar.addWidget(self.welcome)

        layout_content.addWidget(topbar)

        # ========================= STACKED PAGES =========================
        self.stacked = QStackedWidget()

        # -------- Dashboard Admin --------
        self.page_dashboard = QWidget()
        layout_dash = QVBoxLayout(self.page_dashboard)
        title = QLabel("Dashboard Administrador")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet(f"font-size: 28pt; font-weight: 600; color: {COLOR_PRINCIPAL}; padding: 8px;")
        layout_dash.addWidget(title)

        cards = QHBoxLayout()
        self.card_taquilleros = QPushButton("Gestionar\nTaquilleros")
        self.card_taquilleros.setFixedSize(220,140)
        self.card_taquilleros.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                color: {COLOR_TEXTO};
                border-radius: 16px;
                font-size: 14pt;
                font-weight: bold;
                padding: 12px;
                border: 2px solid {COLOR_PRINCIPAL};
            }}
            QPushButton:hover {{
                background-color: #fff9e5;
            }}
        """)
        cards.addWidget(self.card_taquilleros)
        layout_dash.addLayout(cards)
        self.stacked.addWidget(self.page_dashboard)

        # -------- Configuración --------
        self.page_config = QWidget()
        layout_config = QVBoxLayout(self.page_config)
        layout_config.setAlignment(Qt.AlignTop)
        layout_config.setContentsMargins(20,20,20,20)

        titulo_config = QLabel("Configuración de Usuario")
        titulo_config.setAlignment(Qt.AlignCenter)
        titulo_config.setStyleSheet(f"font-size: 16pt; font-weight: bold; color: {COLOR_PRINCIPAL}; margin-bottom: 12px;")
        layout_config.addWidget(titulo_config)

        # Campos de configuración
        layout_config.addWidget(QLabel("Nombre:"))
        self.config_nombre = QLineEdit(self.usuario_actual.get('taqNombre',''))
        layout_config.addWidget(self.config_nombre)

        layout_config.addWidget(QLabel("Primer Apellido:"))
        self.config_ap1 = QLineEdit(self.usuario_actual.get('taqPrimerApell',''))
        layout_config.addWidget(self.config_ap1)

        layout_config.addWidget(QLabel("Segundo Apellido:"))
        self.config_ap2 = QLineEdit(self.usuario_actual.get('taqSegundoApell',''))
        layout_config.addWidget(self.config_ap2)

        layout_config.addWidget(QLabel("Usuario:"))
        self.config_usuario = QLineEdit(self.usuario_actual.get('usuario',''))
        layout_config.addWidget(self.config_usuario)

        layout_config.addWidget(QLabel("Contraseña:"))
        self.config_pass = QLineEdit(self.usuario_actual.get('contraseña',''))
        self.config_pass.setEchoMode(QLineEdit.Password)
        layout_config.addWidget(self.config_pass)

        btn_guardar = QPushButton("Guardar Cambios")
        btn_guardar.setStyleSheet(f"background-color: {COLOR_PRINCIPAL}; color:white; font-weight:bold; padding:8px; margin-top:10px;")
        layout_config.addWidget(btn_guardar)

        def guardar_cambios():
            nombre = self.config_nombre.text().strip()
            ap1 = self.config_ap1.text().strip()
            ap2 = self.config_ap2.text().strip()
            usuario = self.config_usuario.text().strip()
            contrasena = self.config_pass.text().strip()
            if not (nombre and ap1 and usuario and contrasena):
                QMessageBox.warning(self, "Atención", "Los campos obligatorios no pueden estar vacíos")
                return
            ok, err = actualizar_taquillero_bd(
                self.usuario_actual.get('registro'), nombre, ap1, ap2, usuario, contrasena
            )
            if ok:
                QMessageBox.information(self, "Éxito", "Datos actualizados correctamente")
                self.usuario_actual.update({
                    'taqNombre': nombre,
                    'taqPrimerApell': ap1,
                    'taqSegundoApell': ap2,
                    'usuario': usuario,
                    'contraseña': contrasena
                })
                self.welcome.setText(f"Hola, {nombre} {ap1} {ap2}")
                self.stacked.setCurrentWidget(self.page_dashboard)
            else:
                QMessageBox.critical(self, "Error", f"No se pudo actualizar: {err}")

        btn_guardar.clicked.connect(guardar_cambios)
        self.stacked.addWidget(self.page_config)

        layout_content.addWidget(self.stacked)
        layout_main.addWidget(self.sidebar)
        layout_main.addWidget(main_content)
        self.setCentralWidget(central)

        # ========================= EVENTOS =========================
        self.btn_logout.clicked.connect(self.cerrar_sesion)
        self.btn_toggle.clicked.connect(self.toggle_menu)
        self.btn_config.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page_config))

    # ========================= FUNCIONES =========================
    def toggle_menu(self):
        if self.menu_colapsado:
            self.sidebar.setFixedWidth(260)
            self.brand.setText("Rutas Baja Express")
        else:
            self.sidebar.setFixedWidth(64)
            self.brand.setText("RBE")
        self.menu_colapsado = not self.menu_colapsado

    def cerrar_sesion(self):
        confirm = QMessageBox.question(self, "Confirmar", "¿Cerrar sesión?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.close()
            self.volver_callback()
