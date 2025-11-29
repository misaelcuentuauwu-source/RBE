# panel_principal.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QStackedWidget, QFrame, QSizePolicy, QSpacerItem, QMessageBox
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QFont
from pasajero import VentanaRegistroPasajero
from epilepsia import VentanaAnimada
from terminales import VentanaTerminales
from rutas_baja_express_ui import MainWindow as VentanaVentaBoletos
from conexion import crear_conexion

# ===============================
# Función para actualizar taquillero
# ===============================
def actualizar_taquillero_bd(registro, usuario, contrasena):
    try:
        cn = crear_conexion()
        cur = cn.cursor()
        cur.execute("""
            UPDATE taquillero
            SET usuario=%s, contraseña=%s
            WHERE registro=%s
        """, (usuario, contrasena, registro))
        cn.commit()
        cur.close()
        cn.close()
        return True, None
    except Exception as e:
        return False, str(e)

# ===============================
# Sidebar Animado
# ===============================
class SidebarAnimado(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._width = 260
        self.setFixedWidth(self._width)
        
    def get_width(self):
        return self._width
    
    def set_width(self, width):
        self._width = width
        self.setFixedWidth(int(width))
    
    width_prop = Property(int, get_width, set_width)

# ===============================
# Panel Principal
# ===============================
class PanelPrincipal(QMainWindow):
    def __init__(self, usuario_actual, volver_callback):
        super().__init__()
        self.usuario_actual = usuario_actual or {}
        self.volver_callback = volver_callback
        self.menu_colapsado = False

        # Colores corporativos
        self.COLOR_FONDO = "#f2f2f2"
        self.COLOR_PRINCIPAL = "#1181c3"
        self.COLOR_NARANJA = "#ed7237"
        self.COLOR_TEXTO = "#2b2b2b"

        self.setWindowTitle("Rutas Baja Express - Panel")
        # Tamaño inicial más compacto y horizontal
        self.setGeometry(100, 100, 1200, 650)
        self.setMinimumSize(900, 500)  # Tamaño mínimo para que no se deforme
        self.setStyleSheet(f"background-color: {self.COLOR_FONDO}; font-family: 'Segoe UI';")

        # ========================= CONTENEDOR PRINCIPAL =========================
        central = QWidget()
        self.layout_main = QHBoxLayout(central)
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)

        # ========================= SIDEBAR ANIMADO =========================
        self.sidebar = SidebarAnimado()
        self.sidebar.setStyleSheet(f"background-color: {self.COLOR_NARANJA};")
        self.layout_sidebar = QVBoxLayout(self.sidebar)
        self.layout_sidebar.setContentsMargins(0, 0, 0, 0)
        self.layout_sidebar.setSpacing(0)

        # Contenedor del texto de marca
        brand_container = QWidget()
        brand_layout = QVBoxLayout(brand_container)
        brand_layout.setContentsMargins(12, 16, 12, 16)
        
        self.brand = QLabel("Rutas Baja Express")
        self.brand.setStyleSheet("color: white; font-size: 16pt; font-weight: bold;")
        self.brand.setWordWrap(True)
        self.brand.setAlignment(Qt.AlignCenter)
        brand_layout.addWidget(self.brand)
        
        self.layout_sidebar.addWidget(brand_container)

        # Contenedor de botones
        buttons_container = QWidget()
        self.buttons_layout = QVBoxLayout(buttons_container)
        self.buttons_layout.setContentsMargins(8, 8, 8, 8)
        self.buttons_layout.setSpacing(8)

        # Botón de navegación
        def nav_button(text, icon_collapsed=""):
            btn = QPushButton(text)
            btn.setObjectName("btn_nav")
            btn.setProperty("icon_text", icon_collapsed)  # Guardar texto colapsado
            btn.setProperty("full_text", text)  # Guardar texto completo
            btn.setStyleSheet(f"""
                QPushButton#btn_nav {{
                    background-color: white;
                    color: {self.COLOR_NARANJA};
                    border: none;
                    text-align: left;
                    padding: 12px 18px;
                    font-size: 11pt;
                    border-radius: 8px;
                    margin: 0px;
                    font-weight: 500;
                }}
                QPushButton#btn_nav:hover {{
                    background-color: #ffe3d5;
                    color: {self.COLOR_PRINCIPAL};
                }}
            """)
            return btn

        self.btn_terminales = nav_button("🏢 Terminales", "🏢")
        self.btn_vender = nav_button("🎫 Vender boletos", "🎫")
        self.btn_config = nav_button("⚙️ Configuración", "⚙️")
        self.btn_epilepsia = nav_button("🎮 Epilepsia", "🎮")

        self.buttons_layout.addWidget(self.btn_terminales)
        self.buttons_layout.addWidget(self.btn_vender)
        self.buttons_layout.addWidget(self.btn_config)
        self.buttons_layout.addWidget(self.btn_epilepsia)
        
        self.layout_sidebar.addWidget(buttons_container)
        self.layout_sidebar.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botón cerrar sesión
        logout_container = QWidget()
        logout_layout = QVBoxLayout(logout_container)
        logout_layout.setContentsMargins(12, 12, 12, 12)
        
        self.btn_logout = QPushButton("🚪 Cerrar sesión")
        self.btn_logout.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.COLOR_PRINCIPAL};
                color: white;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: #0d6ca4;
            }}
        """)
        logout_layout.addWidget(self.btn_logout)
        self.layout_sidebar.addWidget(logout_container)

        # ========================= ÁREA DE CONTENIDO =========================
        main_content = QFrame()
        main_content.setStyleSheet(f"background-color: {self.COLOR_FONDO};")
        layout_content = QVBoxLayout(main_content)
        layout_content.setContentsMargins(0, 0, 0, 0)
        layout_content.setSpacing(0)

        # Topbar
        topbar = QFrame()
        topbar.setMaximumHeight(70)
        topbar.setStyleSheet("background-color: white; border-bottom: 2px solid #e0e0e0;")
        layout_topbar = QHBoxLayout(topbar)
        layout_topbar.setContentsMargins(20, 10, 20, 10)

        self.btn_toggle = QPushButton("☰")
        self.btn_toggle.setFixedSize(40, 40)
        self.btn_toggle.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.COLOR_PRINCIPAL};
                color: white;
                border-radius: 10px;
                font-size: 18pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #0d6ca4;
            }}
        """)
        layout_topbar.addWidget(self.btn_toggle)
        layout_topbar.addSpacing(20)

        # Texto de bienvenida
        taq_nombre = self.usuario_actual.get('taqNombre','')
        taq_primer = self.usuario_actual.get('taqPrimerApell','')
        taq_seg = self.usuario_actual.get('taqSegundoApell','')
        self.welcome = QLabel(f"👋 Hola, {taq_nombre} {taq_primer} {taq_seg}")
        self.welcome.setStyleSheet(f"font-size: 12pt; color: {self.COLOR_TEXTO}; font-weight: 500;")
        layout_topbar.addWidget(self.welcome)
        layout_topbar.addStretch()

        search = QLineEdit()
        search.setPlaceholderText("🔍 Buscar...")
        search.setStyleSheet("""
            QLineEdit {
                background-color: #f5f5f5;
                border: 1px solid #d0d0d0;
                border-radius: 18px;
                padding: 8px 16px;
                min-width: 250px;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 2px solid #1181c3;
                background-color: white;
            }
        """)
        layout_topbar.addWidget(search)

        # ========================= STACKED PAGES =========================
        self.stacked = QStackedWidget()
        self.stacked.setStyleSheet(f"background-color: {self.COLOR_FONDO};")

        # -------- Dashboard --------
        self.page_dashboard = QWidget()
        layout_dash = QVBoxLayout(self.page_dashboard)
        layout_dash.setContentsMargins(30, 30, 30, 30)
        layout_dash.setSpacing(20)
        
        title = QLabel("📊 Dashboard")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet(f"font-size: 32pt; font-weight: 600; color: {self.COLOR_PRINCIPAL}; padding: 8px;")
        layout_dash.addWidget(title)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        self.card_registro = QPushButton("👤\nRegistrar\nPasajero")
        self.card_registro.setFixedSize(240, 160)
        self.card_registro.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                color: {self.COLOR_TEXTO};
                border-radius: 20px;
                font-size: 15pt;
                font-weight: bold;
                padding: 16px;
                border: 3px solid {self.COLOR_PRINCIPAL};
            }}
            QPushButton:hover {{
                background-color: #e4f3ff;
                border: 3px solid {self.COLOR_NARANJA};
            }}
        """)
        
        card_stats = QLabel("📈\n\nEstadísticas\nPróximamente")
        card_stats.setFixedSize(240, 160)
        card_stats.setAlignment(Qt.AlignCenter)
        card_stats.setStyleSheet(f"""
            QLabel {{
                background-color: white;
                color: #999;
                border-radius: 20px;
                font-size: 13pt;
                font-weight: bold;
                padding: 16px;
                border: 3px solid #e0e0e0;
            }}
        """)
        
        cards_layout.addWidget(self.card_registro)
        cards_layout.addWidget(card_stats)
        cards_layout.addStretch()
        
        layout_dash.addLayout(cards_layout)
        layout_dash.addStretch()
        self.stacked.addWidget(self.page_dashboard)

        # -------- Configuración --------
        self.page_config = QWidget()
        layout_config = QVBoxLayout(self.page_config)
        layout_config.setAlignment(Qt.AlignTop)
        layout_config.setContentsMargins(40, 40, 40, 40)
        layout_config.setSpacing(16)

        titulo_config = QLabel("⚙️ Configuración de Usuario")
        titulo_config.setAlignment(Qt.AlignLeft)
        titulo_config.setStyleSheet(f"font-size: 24pt; font-weight: bold; color: {self.COLOR_PRINCIPAL}; margin-bottom: 20px;")
        layout_config.addWidget(titulo_config)

        # Card contenedor
        config_card = QFrame()
        config_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                padding: 20px;
            }
        """)
        config_card_layout = QVBoxLayout(config_card)
        config_card_layout.setSpacing(16)

        # Campos estáticos
        def add_field_readonly(label_text, value):
            lbl = QLabel(label_text)
            lbl.setStyleSheet("font-weight: bold; color: #666; font-size: 10pt;")
            val = QLabel(value)
            val.setStyleSheet("font-size: 11pt; color: #333; padding: 8px; background: #f5f5f5; border-radius: 8px;")
            config_card_layout.addWidget(lbl)
            config_card_layout.addWidget(val)

        add_field_readonly("📝 Nombre:", self.usuario_actual.get('taqNombre',''))
        add_field_readonly("📄 Primer Apellido:", self.usuario_actual.get('taqPrimerApell',''))
        add_field_readonly("📄 Segundo Apellido:", self.usuario_actual.get('taqSegundoApell',''))

        # Campos editables
        def add_field_editable(label_text, widget):
            lbl = QLabel(label_text)
            lbl.setStyleSheet("font-weight: bold; color: #666; font-size: 10pt; margin-top: 8px;")
            widget.setStyleSheet("""
                QLineEdit {
                    font-size: 11pt;
                    padding: 10px;
                    border: 2px solid #d0d0d0;
                    border-radius: 8px;
                    background: white;
                }
                QLineEdit:focus {
                    border: 2px solid #1181c3;
                }
            """)
            config_card_layout.addWidget(lbl)
            config_card_layout.addWidget(widget)

        self.config_usuario = QLineEdit(self.usuario_actual.get('usuario',''))
        self.config_pass = QLineEdit(self.usuario_actual.get('contraseña',''))
        self.config_pass.setEchoMode(QLineEdit.Password)

        add_field_editable("👤 Usuario:", self.config_usuario)
        add_field_editable("🔒 Contraseña:", self.config_pass)

        # Botón Guardar
        self.btn_guardar = QPushButton("💾 Guardar Cambios")
        self.btn_guardar.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.COLOR_PRINCIPAL};
                color: white;
                font-weight: bold;
                font-size: 12pt;
                padding: 14px;
                border-radius: 10px;
                margin-top: 20px;
            }}
            QPushButton:hover {{
                background-color: #0d6ca4;
            }}
        """)
        config_card_layout.addWidget(self.btn_guardar)

        layout_config.addWidget(config_card)
        layout_config.addStretch()

        def guardar_cambios():
            usuario = self.config_usuario.text().strip()
            contrasena = self.config_pass.text().strip()
            if not (usuario and contrasena):
                QMessageBox.warning(self, "Atención", "Los campos obligatorios no pueden estar vacíos")
                return
            ok, err = actualizar_taquillero_bd(
                self.usuario_actual.get('registro'), usuario, contrasena
            )
            if ok:
                QMessageBox.information(self, "Éxito", "Datos actualizados correctamente")
                self.usuario_actual.update({'usuario': usuario, 'contraseña': contrasena})
                self.stacked.setCurrentWidget(self.page_dashboard)
            else:
                QMessageBox.critical(self, "Error", f"No se pudo actualizar: {err}")

        self.btn_guardar.clicked.connect(guardar_cambios)
        self.stacked.addWidget(self.page_config)

        # ========================= FIN STACKED =========================
        layout_content.addWidget(topbar)
        layout_content.addWidget(self.stacked)

        self.layout_main.addWidget(self.sidebar)
        self.layout_main.addWidget(main_content, stretch=1)
        self.setCentralWidget(central)

        # ========================= ANIMACIÓN =========================
        self.animation = QPropertyAnimation(self.sidebar, b"width_prop")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        # ========================= EVENTOS =========================
        self.card_registro.clicked.connect(self.abrir_registro_pasajero)
        self.btn_terminales.clicked.connect(self.abrir_terminales)
        self.btn_vender.clicked.connect(self.abrir_venta)
        self.btn_epilepsia.clicked.connect(self.abrir_epilepsia)
        self.btn_logout.clicked.connect(self.cerrar_sesion)
        self.btn_toggle.clicked.connect(self.toggle_menu)
        self.btn_config.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page_config))

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

    def abrir_venta(self):
        """Abre la ventana de venta de boletos"""
        try:
            self.ventana_venta = VentanaVentaBoletos()
            self.ventana_venta.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir venta de boletos:\n{e}")

    def toggle_menu(self):
        """Anima el menú para colapsar/expandir"""
        if self.animation.state() == QPropertyAnimation.Running:
            return
        
        if self.menu_colapsado:
            # Expandir
            self.animation.setStartValue(70)
            self.animation.setEndValue(260)
            self.brand.setText("Rutas Baja Express")
            
            # Restaurar texto completo de botones
            for btn in [self.btn_terminales, self.btn_vender, self.btn_config, self.btn_epilepsia]:
                btn.setText(btn.property("full_text"))
            
            self.btn_logout.setText("🚪 Cerrar sesión")
        else:
            # Colapsar
            self.animation.setStartValue(260)
            self.animation.setEndValue(70)
            self.brand.setText("RBE")
            
            # Cambiar a solo iconos
            for btn in [self.btn_terminales, self.btn_vender, self.btn_config, self.btn_epilepsia]:
                btn.setText(btn.property("icon_text"))
            
            self.btn_logout.setText("🚪")
        
        self.animation.start()
        self.menu_colapsado = not self.menu_colapsado

    def cerrar_sesion(self):
        confirm = QMessageBox.question(
            self, "Confirmar", "¿Cerrar sesión?", 
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.close()
            if self.volver_callback:
                self.volver_callback()