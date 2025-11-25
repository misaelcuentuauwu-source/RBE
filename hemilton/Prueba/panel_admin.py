from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QFrame, QSizePolicy, QSpacerItem, QMessageBox,
    QLineEdit, QComboBox
)
from PySide6.QtCore import Qt
from conexion import crear_conexion


# ===========================================================
# --- UTIL BD ---
# ===========================================================
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


# ===========================================================
# CARD GENÉRICO (vista bonita)
# ===========================================================
class CardEntidad(QWidget):
    def __init__(self, title, insert_callback=None, modify_callback=None, delete_callback=None, read_callback=None):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)

        # title
        lbl = QLabel(title)
        lbl.setStyleSheet("""
            font-size: 22pt;
            font-weight: 700;
            color: #ffa600;
        """)
        layout.addWidget(lbl)

        btns = QHBoxLayout()
        def mkbtn(txt, color):
            b = QPushButton(txt)
            b.setStyleSheet(f"""
                QPushButton {{
                    background: {color};
                    color: white;
                    padding: 8px 14px;
                    border-radius: 8px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: #333333;
                }}
            """)
            return b

        if insert_callback:
            b = mkbtn("➕ Insertar", "#52b788")
            b.clicked.connect(insert_callback)
            btns.addWidget(b)

        if modify_callback:
            b = mkbtn("✏️ Modificar", "#ffb703")
            b.clicked.connect(modify_callback)
            btns.addWidget(b)

        if delete_callback:
            b = mkbtn("🗑 Eliminar", "#e63946")
            b.clicked.connect(delete_callback)
            btns.addWidget(b)

        if read_callback:
            b = mkbtn("👁 Leer", "#457b9d")
            b.clicked.connect(read_callback)
            btns.addWidget(b)

        layout.addLayout(btns)


# ===========================================================
# PANEL ADMIN
# ===========================================================
class PanelAdministrador(QMainWindow):
    def __init__(self, usuario_actual, volver_callback):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.volver_callback = volver_callback

        # ======== UI BASE ========
        self.setWindowTitle("Rutas Baja Express — Administrador")
        self.setGeometry(200, 80, 1050, 680)
        self.setStyleSheet("font-family: Segoe UI; background:#f2f2f2;")

        cont = QWidget()
        ly = QHBoxLayout(cont)

        # ======== SIDEBAR ========
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(210)
        self.sidebar.setStyleSheet("background:#ff8c00;")
        sb = QVBoxLayout(self.sidebar)

        brand = QLabel("ADMIN RBE")
        brand.setStyleSheet("color:white;font-size:18pt;font-weight:bold;padding:16px;")
        sb.addWidget(brand)

        def nav(text, event):
            b = QPushButton(text)
            b.setStyleSheet("""
                QPushButton {
                    background:white;
                    color:#ff8c00;
                    margin:6px 12px;
                    padding:8px 16px;
                    border-radius:8px;
                    font-weight:600;
                    text-align:left;
                }
                QPushButton:hover{
                    background:#ffe7c2;
                }
            """)
            b.clicked.connect(event)
            return b

        self.btn_dash = nav("Dashboard", lambda: self.stacked.setCurrentWidget(self.pg_dashboard))
        self.btn_config = nav("Configuración", lambda: self.stacked.setCurrentWidget(self.pg_config))

        sb.addWidget(self.btn_dash)
        sb.addWidget(self.btn_config)
        sb.addSpacerItem(QSpacerItem(10,10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # cerrar sesión
        logout = QPushButton("Cerrar sesión")
        logout.setStyleSheet("""
            QPushButton{
                background:#f2e800;
                color:#202020;
                margin:10px;
                padding:10px;
                border-radius:8px;
                font-weight:800;
            }
        """)
        logout.clicked.connect(self.logout)
        sb.addWidget(logout)

        # ======== CONTENIDO ========
        content = QVBoxLayout()
        self.stacked = QStackedWidget()

        # ----------------------------------
        # PAGE DASHBOARD
        # ----------------------------------
        self.pg_dashboard = QWidget()
        dash = QVBoxLayout(self.pg_dashboard)
        dash.setContentsMargins(26,26,26,26)

        t = QLabel("Panel Administrativo")
        t.setStyleSheet("font-size:26pt;font-weight:700;color:#ff8c00;")
        dash.addWidget(t)

        # Grid visual
        grid = QVBoxLayout()
        dash.addLayout(grid)

        # CREA CARDS POR TABLA (19)
        tablas = [
            "marca","conductor","ciudad","tipo_asiento","tipo_pasajero","tipo_pago","edo_viaje",
            "pasajero","modelo","terminal","ruta","autobus","viaje","asiento","viaje_asiento",
            "taquillero","pago","ticket"
        ]

        for tb in tablas:
            grid.addWidget(
                CardEntidad(
                    title=f"Tabla: {tb}",
                    insert_callback=lambda tb=tb: self.show_form(tb, "insert"),
                    modify_callback=lambda tb=tb: self.show_form(tb, "update"),
                    delete_callback=lambda tb=tb: self.show_form(tb, "delete"),
                    read_callback=lambda tb=tb: self.show_form(tb, "read")
                )
            )

        self.stacked.addWidget(self.pg_dashboard)

        # ----------------------------------
        # PAGE CONFIGURACIÓN
        # ----------------------------------
        self.pg_config = QWidget()
        cfg = QVBoxLayout(self.pg_config)
        cfg.setContentsMargins(40,40,40,40)

        title = QLabel("Configuración de cuenta")
        title.setStyleSheet("font-size:20pt;font-weight:700;color:#ff8c00;")
        cfg.addWidget(title)

        # DATOS (solo lectura)
        for label, key in [
            ("Nombre", "taqNombre"),
            ("Primer Apellido", "taqPrimerApell"),
            ("Segundo Apellido", "taqSegundoApell"),
        ]:
            l = QLabel(f"{label}: {self.usuario_actual.get(key,'')}")
            l.setStyleSheet("font-size:12pt;color:#333;padding:6px;")
            cfg.addWidget(l)

        # USUARIO y CONTRASEÑA editables
        cfg.addWidget(QLabel("\nUsuario:"))
        self.ed_user = QLineEdit(self.usuario_actual.get('usuario', ''))

        cfg.addWidget(self.ed_user)

        cfg.addWidget(QLabel("Contraseña:"))
        self.ed_pass = QLineEdit(self.usuario_actual.get('contraseña', ''))
        self.ed_pass.setEchoMode(QLineEdit.Password)
        cfg.addWidget(self.ed_pass)

        btn = QPushButton("Guardar cambios")
        btn.setStyleSheet("background:#f2e800;padding:10px;font-weight:700;border-radius:8px;")
        btn.clicked.connect(self.save_config)
        cfg.addWidget(btn)

        self.stacked.addWidget(self.pg_config)

        content.addWidget(self.stacked)
        ly.addWidget(self.sidebar)
        ly.addLayout(content)
        self.setCentralWidget(cont)


    # ===========================================================
    def show_form(self, tabla, modo):
        QMessageBox.information(self, "Vista Form", f"Aquí iría formulario bonito de:\n{tabla}\nModo: {modo}\n(Sin tablas Excel)")

    def save_config(self):
        if not self.ed_user.text() or not self.ed_pass.text():
            QMessageBox.warning(self, "Atención", "Usuario/Contraseña no pueden estar vacíos.")
            return

        ok, err = actualizar_taquillero_bd(
            self.usuario_actual['registro'],
            self.ed_user.text(),
            self.ed_pass.text()
        )

        if ok:
            QMessageBox.information(self, "OK", "Datos actualizados.")
            self.usuario_actual['usuario'] = self.ed_user.text()
            self.usuario_actual['contraseña'] = self.ed_pass.text()
            self.stacked.setCurrentWidget(self.pg_dashboard)
        else:
            QMessageBox.critical(self, "Error", err)

    def logout(self):
        if QMessageBox.question(self,"Salir","¿Cerrar sesión?",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes:
            self.close()
            self.volver_callback()
