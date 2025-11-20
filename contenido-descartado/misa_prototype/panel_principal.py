from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QStackedWidget, QFrame, QSizePolicy, QSpacerItem, QMessageBox
)
from PySide6.QtCore import Qt
from pasajero import VentanaRegistroPasajero   # ⭐ IMPORTANTE
from epilepsia import VentanaAnimada
from terminales import VentanaTerminales


class PanelPrincipal(QMainWindow):
    def __init__(self, usuario_actual, volver_callback):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.volver_callback = volver_callback
        self.menu_colapsado = False

        # Colores corporativos
        COLOR_FONDO = "#f2f2f2"
        COLOR_PRINCIPAL = "#1181c3"
        COLOR_NARANJA = "#ed7237"
        COLOR_TEXTO = "#2b2b2b"

        self.setWindowTitle("Rutas Baja Express - Panel")
        self.setGeometry(100, 100, 1000, 640)
        self.setStyleSheet(f"background-color: {COLOR_FONDO}; font-family: 'Segoe UI';")

        # =========================  CONTENEDOR PRINCIPAL  =========================
        central = QWidget()
        layout_main = QHBoxLayout(central)

        # =========================  SIDEBAR LATERAL IZQUIERDA  =========================
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(260)
        self.sidebar.setStyleSheet(f"background-color: {COLOR_NARANJA};")
        layout_sidebar = QVBoxLayout(self.sidebar)

        self.brand = QLabel("Rutas Baja Express")
        self.brand.setStyleSheet("color: white; font-size: 16pt; font-weight: bold; padding: 16px;")
        layout_sidebar.addWidget(self.brand)

        # --------------------  BOTONES DEL SIDEBAR --------------------
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
                    background-color: #ffe3d5;
                    color: {COLOR_PRINCIPAL};
                }}
            """)
            return btn

        self.btn_terminales = nav_button("Terminales disponibles")
        self.btn_epilepsia = nav_button("Epilepsia")
        self.btn_config = nav_button("Configuración")

        layout_sidebar.addWidget(self.btn_terminales)
        layout_sidebar.addWidget(self.btn_config)
        layout_sidebar.addWidget(self.btn_epilepsia)
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
                background-color: #0d6ca4;
            }}
        """)
        layout_sidebar.addWidget(self.btn_logout)

        # =========================  ÁREA DE CONTENIDO  =========================
        main_content = QFrame()
        layout_content = QVBoxLayout(main_content)

        # -------------------  TOPBAR -------------------
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
                background-color: #0d6ca4;
            }}
        """)

        layout_topbar.addWidget(self.btn_toggle)
        layout_topbar.addStretch()

        welcome = QLabel(f"Hola, {self.usuario_actual['taqnombre']} {self.usuario_actual['taqprimerapell']}")
        welcome.setStyleSheet(f"font-size: 11pt; color: {COLOR_TEXTO};")
        layout_topbar.addWidget(welcome)

        search = QLineEdit()
        search.setPlaceholderText("Buscar...")
        search.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #d0d0d0;
                border-radius: 14px;
                padding: 6px 10px;
                min-width: 220px;
            }
        """)
        layout_topbar.addWidget(search)

        # =========================  STACKED PAGES =========================
        self.stacked = QStackedWidget()

        # ----------------------  DASHBOARD  ----------------------
        self.page_dashboard = QWidget()
        layout_dash = QVBoxLayout(self.page_dashboard)

        title = QLabel("Dashboard")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet(f"font-size: 28pt; font-weight: 600; color: {COLOR_PRINCIPAL}; padding: 8px;")
        layout_dash.addWidget(title)

        # ----------------------  TARJETAS / CUBOS  ----------------------
        cards = QHBoxLayout()

        # Tarjeta Registrar Pasajero
        self.card_registro = QPushButton("Registrar\nPasajero")
        self.card_registro.setFixedSize(220, 140)
        self.card_registro.setStyleSheet(f"""
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
                background-color: #e4f3ff;
            }}
        """)

        cards.addWidget(self.card_registro)
        layout_dash.addLayout(cards)

        self.stacked.addWidget(self.page_dashboard)

        # ========================= FIN STACKED =========================
        layout_content.addWidget(topbar)
        layout_content.addWidget(self.stacked)

        layout_main.addWidget(self.sidebar)
        layout_main.addWidget(main_content)
        self.setCentralWidget(central)

        # ========================= EVENTOS =========================

        self.card_registro.clicked.connect(self.abrir_registro_pasajero)
        self.btn_terminales.clicked.connect(self.abrir_terminales)
        self.btn_epilepsia.clicked.connect(self.abrir_epilepsia)
        self.btn_logout.clicked.connect(self.cerrar_sesion)
        self.btn_toggle.clicked.connect(self.toggle_menu)

    # ========================= FUNCIONES =========================

    def abrir_registro_pasajero(self):
        self.ventana_registro = VentanaRegistroPasajero()
        self.ventana_registro.show()

    def abrir_terminales(self):
        self.ventana_terminales = VentanaTerminales()
        self.ventana_terminales.show()

    def abrir_epilepsia(self):
        self.ventana_epilepsia = VentanaAnimada()
        self.ventana_epilepsia.show()
        self.close()

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
