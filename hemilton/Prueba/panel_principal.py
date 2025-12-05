from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QStackedWidget, QFrame, QSizePolicy, QSpacerItem, QMessageBox,
    QScrollArea
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QFont
from pasajero import VentanaRegistroPasajero
from epilepsia import VentanaAnimada
from terminales import VentanaTerminales
from rutas_baja_express_ui import MainWindow as VentanaVentaBoletos
from gestionviajes import MainWindow as VentanaHistorialViajes
from conexion import crear_conexion

## Actualizar tauqillero ##
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

## Sidebar ##
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

## Panel inicial ##
class PanelPrincipal(QMainWindow):
    def __init__(self, usuario_actual, volver_callback):
        super().__init__()
        self.usuario_actual = usuario_actual or {}
        self.volver_callback = volver_callback
        self.menu_colapsado = False

        ## Colores corporativos ##
        self.COLOR_FONDO = "#f2f2f2"
        self.COLOR_PRINCIPAL = "#1181c3"
        self.COLOR_NARANJA = "#ed7237"
        self.COLOR_TEXTO = "#2b2b2b"

        self.setWindowTitle("Rutas Baja Express - Panel")
        self.setGeometry(100, 100, 1200, 650)
        self.setMinimumSize(900, 500)
        self.setStyleSheet(f"background-color: {self.COLOR_FONDO}; font-family: 'Segoe UI';")

        ## Contenedor principal ##
        central = QWidget()
        self.layout_main = QHBoxLayout(central)
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)

        ## Sidebar animado ##
        self.sidebar = SidebarAnimado()
        self.sidebar.setStyleSheet(f"background-color: {self.COLOR_NARANJA};")
        self.layout_sidebar = QVBoxLayout(self.sidebar)
        self.layout_sidebar.setContentsMargins(0, 0, 0, 0)
        self.layout_sidebar.setSpacing(0)

        ## Contenedor del texto ##
        brand_container = QWidget()
        brand_layout = QVBoxLayout(brand_container)
        brand_layout.setContentsMargins(12, 16, 12, 16)

        self.brand = QLabel("Rutas Baja Express")
        self.brand.setStyleSheet("color: white; font-size: 16pt; font-weight: bold;")
        self.brand.setWordWrap(True)
        self.brand.setAlignment(Qt.AlignCenter)
        brand_layout.addWidget(self.brand)

        self.layout_sidebar.addWidget(brand_container)

        ## Contenedor de botones ##
        buttons_container = QWidget()
        self.buttons_layout = QVBoxLayout(buttons_container)
        self.buttons_layout.setContentsMargins(8, 8, 8, 8)
        self.buttons_layout.setSpacing(8)

        ## Boton de navegacion ##
        def nav_button(text, icon_collapsed=""):
            btn = QPushButton(text)
            btn.setObjectName("btn_nav")
            btn.setProperty("icon_text", icon_collapsed)
            btn.setProperty("full_text", text)
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

        ## Botones de navegacion ##
        self.btn_dashboard = nav_button("🏠 Dashboard", "🏠")
        self.btn_terminales = nav_button("🏢 Terminales", "🏢")
        self.btn_vender = nav_button("🎫 Vender boletos", "🎫")
        self.btn_historial = nav_button("📋 Historial de Viajes", "📋")
        self.btn_config = nav_button("⚙️ Configuración", "⚙️")

        self.buttons_layout.addWidget(self.btn_dashboard)
        self.buttons_layout.addWidget(self.btn_terminales)
        self.buttons_layout.addWidget(self.btn_vender)
        self.buttons_layout.addWidget(self.btn_historial)
        self.buttons_layout.addWidget(self.btn_config)

        self.layout_sidebar.addWidget(buttons_container)
        self.layout_sidebar.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        ## Boton cerrar sesion ##
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

        # # Contenido ##
        main_content = QFrame()
        main_content.setStyleSheet(f"background-color: {self.COLOR_FONDO};")
        layout_content = QVBoxLayout(main_content)
        layout_content.setContentsMargins(0, 0, 0, 0)
        layout_content.setSpacing(0)

        ## Topbar ##
        topbar = QFrame()
        topbar.setMaximumHeight(70)
        topbar.setStyleSheet("""
            background-color: white;
            border-bottom: 1px solid #e0e0e0;
            padding: 0 10px;
        """)
        layout_topbar = QHBoxLayout(topbar)
        layout_topbar.setContentsMargins(10, 5, 10, 5)
        layout_topbar.setSpacing(10)

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
        layout_topbar.addSpacing(10)

        ## Texto de bienvenida ##
        taq_nombre = self.usuario_actual.get('taqNombre','')
        taq_primer = self.usuario_actual.get('taqPrimerApell','')
        taq_seg = self.usuario_actual.get('taqSegundoApell','')
        self.welcome = QLabel(f"👋 Hola, {taq_nombre} {taq_primer} {taq_seg}")
        self.welcome.setStyleSheet(f"font-size: 12pt; color: {self.COLOR_TEXTO}; font-weight: 500;")
        layout_topbar.addWidget(self.welcome)
        layout_topbar.addStretch()

        ## Buscador ##
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Buscar...")
        self.search.setStyleSheet("""
            QLineEdit {
                background-color: #f5f5f5;
                border: 1px solid #d0d0d0;
                border-radius: 18px;
                padding: 8px 16px;
                min-width: 200px;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 1px solid #1181c3;
                background-color: white;
            }
        """)
        self.search.returnPressed.connect(self.buscar_accion)
        layout_topbar.addWidget(self.search)

        ## El stacked ##
        self.stacked = QStackedWidget()
        self.stacked.setStyleSheet(f"background-color: {self.COLOR_FONDO};")

        ## Dashboard ##
        self.page_dashboard = QWidget()
        layout_dash = QVBoxLayout(self.page_dashboard)
        layout_dash.setContentsMargins(20, 20, 20, 20)
        layout_dash.setSpacing(15)

        ## Contenedor scroll ##
        scroll_dash = QScrollArea()
        scroll_dash.setWidgetResizable(True)
        scroll_dash.setStyleSheet("background: transparent; border: none;")

        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setAlignment(Qt.AlignCenter)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(20)

        ## el camion ##
        logo_label = QLabel("🚌")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet(f"""
            QLabel {{
                font-size: 180pt;
                color: {self.COLOR_PRINCIPAL};
                opacity: 0.15;
                padding: 40px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(17, 129, 195, 0.05),
                    stop:1 rgba(237, 114, 55, 0.05)
                );
                border-radius: 30px;
            }}
        """)
        logo_layout.addWidget(logo_label)
 
        # Texto de bienvenida ##
        welcome_text = QLabel("Bienvenido al Sistema de Gestión")
        welcome_text.setAlignment(Qt.AlignCenter)
        welcome_text.setStyleSheet(f"""
            QLabel {{
                font-size: 28pt;
                font-weight: 300;
                color: {self.COLOR_TEXTO};
                margin-top: 20px;
                letter-spacing: 2px;
            }}
        """)
        logo_layout.addWidget(welcome_text)

        ## Subtitulo ##
        subtitle = QLabel("Rutas Baja Express")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: 42pt;
                font-weight: bold;
                color: {self.COLOR_PRINCIPAL};
                margin-top: 10px;
            }}
        """)
        logo_layout.addWidget(subtitle)

        ## Mensaje de relleno ##
        message = QLabel("Selecciona una opción del menú para comenzar")
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet("""
            QLabel {
                font-size: 14pt;
                color: #666;
                margin-top: 20px;
                font-weight: 300;
            }
        """)
        logo_layout.addWidget(message)

        scroll_dash.setWidget(logo_container)
        layout_dash.addWidget(scroll_dash)
        self.stacked.addWidget(self.page_dashboard)

        ## Configuracion ##
        self.page_config = QWidget()
        layout_config = QVBoxLayout(self.page_config)
        layout_config.setAlignment(Qt.AlignTop)
        layout_config.setContentsMargins(20, 20, 20, 20)
        layout_config.setSpacing(12)

        ## Contenedor scroll ##
        scroll_config = QScrollArea()
        scroll_config.setWidgetResizable(True)
        scroll_config.setStyleSheet("background: transparent; border: none;")

        config_content = QWidget()
        config_content_layout = QVBoxLayout(config_content)
        config_content_layout.setContentsMargins(20, 20, 20, 20)
        config_content_layout.setSpacing(16)

        titulo_config = QLabel("⚙️ Configuración de Usuario")
        titulo_config.setAlignment(Qt.AlignLeft)
        titulo_config.setStyleSheet(f"font-size: 20pt; font-weight: bold; color: {self.COLOR_PRINCIPAL}; margin-bottom: 10px;")
        config_content_layout.addWidget(titulo_config)

        ## contenedor carta ##
        self.config_card = QFrame()
        self.config_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
                max-width: 800px;
            }
        """)
        config_card_layout = QVBoxLayout(self.config_card)
        config_card_layout.setSpacing(14)

        ## Campos estaticos ##
        def add_field_readonly(label_text, value):
            lbl = QLabel(label_text)
            lbl.setStyleSheet("font-weight: bold; color: #666; font-size: 10pt;")
            val = QLabel(value)
            val.setStyleSheet("""
                font-size: 11pt;
                color: #333;
                padding: 10px;
                background: #f8f8f8;
                border-radius: 6px;
                border: 1px solid #e0e0e0;
                min-height: 40px;
            """)
            config_card_layout.addWidget(lbl)
            config_card_layout.addWidget(val)

        add_field_readonly("📝 Nombre:", self.usuario_actual.get('taqNombre',''))
        add_field_readonly("📄 Primer Apellido:", self.usuario_actual.get('taqPrimerApell',''))
        add_field_readonly("📄 Segundo Apellido:", self.usuario_actual.get('taqSegundoApell',''))

        ## Campos para editar ##
        def add_field_editable(label_text, widget):
            lbl = QLabel(label_text)
            lbl.setStyleSheet("font-weight: bold; color: #666; font-size: 10pt; margin-top: 8px;")
            widget.setStyleSheet("""
                QLineEdit {
                    font-size: 11pt;
                    padding: 10px;
                    border: 1px solid #d0d0d0;
                    border-radius: 6px;
                    background: white;
                    min-height: 40px;
                }
                QLineEdit:focus {
                    border: 1px solid #1181c3;
                }
            """)
            config_card_layout.addWidget(lbl)
            config_card_layout.addWidget(widget)

        self.config_usuario = QLineEdit(self.usuario_actual.get('usuario',''))
        self.config_pass = QLineEdit(self.usuario_actual.get('contraseña',''))
        self.config_pass.setEchoMode(QLineEdit.Password)

        add_field_editable("👤 Usuario:", self.config_usuario)
        add_field_editable("🔒 Contraseña:", self.config_pass)

        ## Botón Guardar ##
        self.btn_guardar = QPushButton("💾 Guardar Cambios")
        self.btn_guardar.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.COLOR_PRINCIPAL};
                color: white;
                font-weight: bold;
                font-size: 11pt;
                padding: 12px;
                border-radius: 8px;
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: #0d6ca4;
            }}
        """)
        config_card_layout.addWidget(self.btn_guardar)

        config_content_layout.addWidget(self.config_card)
        config_content_layout.addStretch()

        scroll_config.setWidget(config_content)
        layout_config.addWidget(scroll_config)
        self.stacked.addWidget(self.page_config)

        ## Historial ##
        self.page_historial = QWidget()
        self.historial_layout = QVBoxLayout(self.page_historial)
        self.historial_layout.setContentsMargins(0, 0, 0, 0)

        # Contenedor scroll de nuevo ##
        scroll_historial = QScrollArea()
        scroll_historial.setWidgetResizable(True)
        scroll_historial.setStyleSheet("background: transparent; border: none;")

        self.historial_widget = VentanaHistorialViajes()
        self.historial_widget.setWindowFlags(Qt.Widget)
        scroll_historial.setWidget(self.historial_widget)
        self.historial_layout.addWidget(scroll_historial)

        self.stacked.addWidget(self.page_historial)

        ## stakced fin ##
        layout_content.addWidget(topbar)
        layout_content.addWidget(self.stacked)

        self.layout_main.addWidget(self.sidebar)
        self.layout_main.addWidget(main_content, stretch=1)
        self.setCentralWidget(central)

        ## animacion misa ##
        self.animation = QPropertyAnimation(self.sidebar, b"width_prop")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        ## eventos ##
        self.btn_dashboard.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page_dashboard))
        self.btn_terminales.clicked.connect(self.abrir_terminales)
        self.btn_vender.clicked.connect(self.abrir_venta)
        self.btn_historial.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page_historial))
        self.btn_logout.clicked.connect(self.cerrar_sesion)
        self.btn_toggle.clicked.connect(self.toggle_menu)
        self.btn_config.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page_config))
        self.btn_guardar.clicked.connect(self.guardar_cambios)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        ## ajustes de la carta ##
        if hasattr(self, 'config_card'):
            ancho_disponible = self.width() - 300  # Considerando el sidebar
            self.config_card.setMaximumWidth(max(600, ancho_disponible * 0.7))

        ## Ajustar el tamano ##
        if self.width() < 1000:
            self.brand.setStyleSheet("color: white; font-size: 12pt; font-weight: bold;")
            self.welcome.setStyleSheet(f"font-size: 10pt; color: {self.COLOR_TEXTO}; font-weight: 500;")
        else:
            self.brand.setStyleSheet("color: white; font-size: 16pt; font-weight: bold;")
            self.welcome.setStyleSheet(f"font-size: 12pt; color: {self.COLOR_TEXTO}; font-weight: 500;")

    def guardar_cambios(self):
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

    def buscar_accion(self):
        """Busca acciones basadas en palabras clave"""
        texto = self.search.text().strip().lower()

        if not texto:
            return

        acciones = {
            'boleto': self.abrir_venta,
            'boletos': self.abrir_venta,
            'vender': self.abrir_venta,
            'venta': self.abrir_venta,
            'ticket': self.abrir_venta,
            'tickets': self.abrir_venta,
            'terminal': self.abrir_terminales,
            'terminales': self.abrir_terminales,
            'estacion': self.abrir_terminales,
            'estaciones': self.abrir_terminales,
            'pasajero': self.abrir_registro_pasajero,
            'pasajeros': self.abrir_registro_pasajero,
            'registrar': self.abrir_registro_pasajero,
            'registro': self.abrir_registro_pasajero,
            'cliente': self.abrir_registro_pasajero,
            'clientes': self.abrir_registro_pasajero,
            'config': lambda: self.stacked.setCurrentWidget(self.page_config),
            'configuracion': lambda: self.stacked.setCurrentWidget(self.page_config),
            'configuración': lambda: self.stacked.setCurrentWidget(self.page_config),
            'ajustes': lambda: self.stacked.setCurrentWidget(self.page_config),
            'perfil': lambda: self.stacked.setCurrentWidget(self.page_config),
            'inicio': lambda: self.stacked.setCurrentWidget(self.page_dashboard),
            'dashboard': lambda: self.stacked.setCurrentWidget(self.page_dashboard),
            'home': lambda: self.stacked.setCurrentWidget(self.page_dashboard),
            'historial': lambda: self.stacked.setCurrentWidget(self.page_historial),
            'viajes': lambda: self.stacked.setCurrentWidget(self.page_historial),
            'history': lambda: self.stacked.setCurrentWidget(self.page_historial),
            'epilepsia': self.abrir_epilepsia,
            'juego': self.abrir_epilepsia,
            'game': self.abrir_epilepsia,
        }

        encontrado = False
        for palabra_clave, accion in acciones.items():
            if palabra_clave in texto:
                accion()
                self.search.clear()
                encontrado = True
                break

        if not encontrado:
            QMessageBox.information(
                self,
                "Búsqueda",
                f"No se encontró ninguna acción para: '{texto}'\n\n"
                "Prueba con: boleto, terminal, pasajero, historial, config, inicio..."
            )
            self.search.clear()

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
        try:
            # Pasar el usuario actual a la ventana de venta
            self.ventana_venta = VentanaVentaBoletos(taquillero_data=self.usuario_actual)
            self.ventana_venta.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir venta de boletos:\n{e}")
    def toggle_menu(self):
        if self.animation.state() == QPropertyAnimation.Running:
            return

        if self.menu_colapsado:
            self.animation.setStartValue(70)
            self.animation.setEndValue(260)
            self.brand.setText("Rutas Baja Express")

            for btn in [self.btn_dashboard, self.btn_terminales, self.btn_vender, self.btn_historial, self.btn_config]:
                btn.setText(btn.property("full_text"))

            self.btn_logout.setText("🚪 Cerrar sesión")
        else:
            self.animation.setStartValue(260)
            self.animation.setEndValue(70)
            self.brand.setText("RBE")

            for btn in [self.btn_dashboard, self.btn_terminales, self.btn_vender, self.btn_historial, self.btn_config]:
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