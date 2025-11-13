# panel_principal.py
# Ventana principal tras el login

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt


class PanelPrincipal(QWidget):
    def __init__(self, usuario_actual, volver_callback):
        super().__init__()
        self.usuario_actual = usuario_actual
        self.volver_callback = volver_callback
        self.configurar_ui()

    def configurar_ui(self):
        self.setWindowTitle("Rutas Baja Express - Panel Principal")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #f2f2f2; font-family: 'Segoe UI';")

        layout = QVBoxLayout()

        titulo = QLabel("Panel principal")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #1181c3; font-size: 18pt; font-weight: bold; padding: 12px;")
        layout.addWidget(titulo)

        bienvenida = QLabel(f"Bienvenido {self.usuario_actual['taqnombre']} {self.usuario_actual['taqprimerapell']}")
        bienvenida.setAlignment(Qt.AlignCenter)
        layout.addWidget(bienvenida)

        btn_logout = QPushButton("Cerrar sesión")
        btn_logout.setStyleSheet("background-color: #d9534f; color: white; height: 40px; font-weight: bold;")
        btn_logout.clicked.connect(self.cerrar_sesion)
        layout.addWidget(btn_logout, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def cerrar_sesion(self):
        confirm = QMessageBox.question(self, "Confirmar", "¿Cerrar sesión?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.close()
            self.volver_callback()
