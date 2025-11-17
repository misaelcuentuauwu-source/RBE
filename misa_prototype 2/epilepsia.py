from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PySide6.QtCore import Qt, QTimer
import sys
import math

class VentanaAnimada(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚡ EPILEPSIA RGB ⚡")
        self.setGeometry(200, 200, 600, 400)

        # Layout
        layout = QVBoxLayout()
        self.label = QLabel("☠️  EPILEPSIA  ☠️", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 26pt;
            color: white;
            font-weight: bold;
        """)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Variables para animación
        self.t = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animar_fondo)
        self.timer.start(25)  # 40 FPS aprox.

    def animar_fondo(self):
        """Cambia el color del fondo con una ola RGB más suave y fluida"""
        self.t += 0.08

        # Colores tipo ola continua, suaves
        r = int((math.sin(self.t) + 1) * 127)
        g = int((math.sin(self.t + 2) + 1) * 127)
        b = int((math.sin(self.t + 4) + 1) * 127)

        r2 = int((math.sin(self.t + 1) + 1) * 127)
        g2 = int((math.sin(self.t + 3) + 1) * 127)
        b2 = int((math.sin(self.t + 5) + 1) * 127)

        color1 = f"rgb({r}, {g}, {b})"
        color2 = f"rgb({r2}, {g2}, {b2})"

        # Degradado con leve desplazamiento dinámico
        x_shift = abs(math.sin(self.t)) * 0.5 + 0.25
        y_shift = abs(math.cos(self.t)) * 0.5 + 0.25

        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:{x_shift:.2f}, y2:{y_shift:.2f},
                    stop:0 {color1},
                    stop:1 {color2}
                );
            }}
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaAnimada()
    ventana.show()
    sys.exit(app.exec())
