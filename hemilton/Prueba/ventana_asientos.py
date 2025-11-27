# ventana_asientos_pyside6.py
# Interfaz de selección de asientos (4 filas x 9 asientos) - PySide6
# Asientos colocados dentro del camión (posicionamiento absoluto, responsivo)

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QSizePolicy, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QPixmap, QIcon, QFont
import sys
import os
import recursos_rc

# -------------------------
# Util: cargar pixmap con intentos (qrc o archivo local)
# -------------------------
def load_pixmap_try(paths):
    for p in paths:
        if p is None:
            continue
        pm = QPixmap(p)
        if not pm.isNull():
            return pm
        if os.path.exists(p):
            pm2 = QPixmap(p)
            if not pm2.isNull():
                return pm2
    return QPixmap()

class VentanaAsientos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seleccionar asientos - Rutas Baja Express")
        self.resize(1200, 760)

        # --- iconos / pixmaps ---
        self.pm_logo = load_pixmap_try([":/recursos/logocirculo.png", "logocirculo.png"])
        self.pm_mapa = load_pixmap_try([":/recursos/mapa de Baja Califor.png", "mapa de Baja Califor.png"])
        self.pm_camion = load_pixmap_try([":/recursos/autobusmarco.png", "autobusmarco.png"])

        self.icon_disp = load_pixmap_try([":/recursos/asiento.svg", "asiento.svg"])
        self.icon_sel = load_pixmap_try([":/recursos/asientoseleccionado.svg", "asientoseleccionado.svg"])
        self.icon_ocup = load_pixmap_try([":/recursos/asientoocupado.svg", "asientoocupado.svg"])
        self.icon_esp = load_pixmap_try([":/recursos/asientoespecial.svg", "asientoespecial.svg"])
        self.icon_esp_sel = load_pixmap_try([":/recursos/asientoespecialseleccionado.svg", "asientoespecialseleccionado.svg"])

        # Estado de asientos
        self.rows = 4
        self.cols = 9
        self.special_positions = {(2, 1), (3, 1)}
        self.occupied = set()
        self.selected = []

        # ----------------- Layout principal EN SCROLL -----------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        main_container = QWidget()
        scroll.setWidget(main_container)
        self.setCentralWidget(scroll)

        root = QVBoxLayout(main_container)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(10)

        # Header naranja
        header = QFrame()
        header.setStyleSheet("background:#EE733A; border-radius:8px;")
        hh = QHBoxLayout(header)
        hh.setContentsMargins(12, 8, 12, 8)

        lab_logo = QLabel()
        if not self.pm_logo.isNull():
            lab_logo.setPixmap(self.pm_logo.scaled(68, 68, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        lab_logo.setFixedSize(72, 72)
        hh.addWidget(lab_logo)

        title = QLabel("Rutas Baja Express")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: white;")
        hh.addWidget(title, stretch=1)

        lab_map = QLabel()
        if not self.pm_mapa.isNull():
            lab_map.setPixmap(self.pm_mapa.scaled(120, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        lab_map.setFixedSize(120, 72)
        hh.addWidget(lab_map)

        root.addWidget(header)

        # Barra leyenda blanca
        legend = QFrame()
        legend.setStyleSheet("background:white; border-radius:18px;")
        legend.setFixedHeight(84)
        lh = QHBoxLayout(legend)
        lh.setContentsMargins(20, 12, 20, 12)

        lbl = QLabel("Selección de asientos")
        lbl.setFont(QFont("Segoe UI", 14, QFont.Bold))
        lh.addWidget(lbl)
        lh.addSpacing(20)

        def item_ley(text, color):
            w = QLabel(text)
            w.setStyleSheet("color:#666; padding-left:10px;")
            dot = QLabel()
            dot.setFixedSize(18, 18)
            dot.setStyleSheet(f"background:{color}; border-radius:4px;")
            cont = QWidget()
            cont_l = QHBoxLayout(cont)
            cont_l.setContentsMargins(4,0,4,0)
            cont_l.addWidget(dot)
            cont_l.addWidget(w)
            return cont

        lh.addWidget(item_ley("Ocupado", "#7f8c8d"))
        lh.addSpacing(12)
        lh.addWidget(item_ley("Disponible", "#EE733A"))
        lh.addSpacing(12)
        lh.addWidget(item_ley("Especial", "#8E44AD"))
        lh.addSpacing(12)
        lh.addWidget(item_ley("Seleccion", "#F49945"))
        lh.addSpacing(12)
        lh.addWidget(item_ley("Seleccionado", "#1480c4"))
        lh.addSpacing(70)
        # Info de asiento seleccionado (debajo de botones)
        self.info_label = QLabel("Fila: -    Asiento: -")
        self.info_label.setStyleSheet("font-size:13px;")
        lh.addWidget(self.info_label)
        
        lh.addStretch()
        

        root.addWidget(legend)

        # Contenedor Camión
        main_frame = QFrame()
        main_frame.setStyleSheet("background:#0a79b7; border-radius:10px;")
        main_layout = QVBoxLayout(main_frame)
        main_layout.setContentsMargins(12, 12, 12, 12)

        self.camion_label = QLabel()
        self.camion_label.setStyleSheet("background: transparent;")
        if not self.pm_camion.isNull():
            self.camion_label.setPixmap(self.pm_camion)
        # scaledContents True para que la etiqueta muestre el pixmap redimensionado
        self.camion_label.setScaledContents(True)
        # permitir que el contenedor del camión crezca/encoga
        self.camion_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # overlay para asientos (hijos con posicion absoluta sobre camion_label)
        self.overlay = QWidget(self.camion_label)
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.overlay.setStyleSheet("background: transparent;")
        self.overlay.setGeometry(0,0,10,10)

        camion_container = QFrame()
        camion_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        cc_layout = QHBoxLayout(camion_container)
        cc_layout.addWidget(self.camion_label, alignment=Qt.AlignCenter)

        main_layout.addWidget(camion_container)
        root.addWidget(main_frame, stretch=1)

        # -------------------------------------------------
        # IMPORTANTE: un stretch opcional para separación si la ventana es grande
        # -------------------------------------------------
        # root.addStretch(1)   # Lo dejamos comentado para que el scroll se comporte naturalmente

        # ===================== PANEL DE INFORMACIÓN (UNA LINEA) =====================
        info_panel = QFrame()
        info_panel.setStyleSheet("background:white; border-radius:12px; padding:10px;")
        info_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        info_layout = QHBoxLayout(info_panel)
        info_layout.setContentsMargins(10,6,10,6)
        info_layout.setSpacing(20)

        self.lbl_viaje  = QLabel("Número de viaje: -")
        self.lbl_bus    = QLabel("Número de autobús: -")
        self.lbl_fecha  = QLabel("Fecha y hora de salida: -")
        self.lbl_origen = QLabel("Ciudad origen: -")
        self.lbl_dest   = QLabel("Ciudad destino: -")

        for w in (self.lbl_viaje, self.lbl_bus, self.lbl_fecha, self.lbl_origen, self.lbl_dest):
            w.setStyleSheet("font-size:14px; color:#333;")
            w.setMinimumWidth(140)   # ayudar a que se mantengan visibles
            info_layout.addWidget(w)

        # si el espacio no alcanza, el QScrollArea principal permitirá scrollear verticalmente
        root.addWidget(info_panel)

        # Botones inferiores (derecha)
        bottom = QHBoxLayout()
        bottom.addStretch()
        self.btn_accept = QPushButton("Aceptar")
        self.btn_accept.setFixedSize(140, 48)
        self.btn_accept.setStyleSheet("background:#14407C;color:white;border-radius:24px;font-size:15px;")
        self.btn_accept.clicked.connect(self.on_accept)

        btn_back = QPushButton("Regresar")
        btn_back.setFixedSize(140, 48)
        btn_back.setStyleSheet("background:#EE733A;color:white;border-radius:24px;font-size:15px;")
        btn_back.clicked.connect(self.close)

        bottom.addWidget(self.btn_accept)
        bottom.addSpacing(12)
        bottom.addWidget(btn_back)
        root.addLayout(bottom)



        # Crear botones de asientos (hijos del overlay)
        self.seat_buttons = {}
        counter = 1
        for r in range(1, self.rows+1):
            for c in range(1, self.cols+1):
                btn = QPushButton(str(counter), self.overlay)
                btn.setCheckable(True)
                btn.setStyleSheet("border:none; background:transparent;")
                # conectar con captura de fila/col evitando late binding
                btn.clicked.connect(lambda checked, rr=r, cc=c, b=btn: self.on_seat_clicked(rr, cc, b))
                self.seat_buttons[(r,c)] = btn
                counter += 1

        # Referencias internas del camión (tu referencia original)
        self.ref_camion_w = 600.0
        self.ref_camion_h = 185.0
        self.ref_interior = QRect(78, 18, 503, 148)

        # llamada inicial para posicionar todo
        self._update_camion_and_overlay()

    # ---------------------------------------
    def _update_camion_and_overlay(self):
        """Ajusta tamaño de la camion_label y posiciona los asientos.
           Evita que los asientos se salgan: si la ventana es muy pequeña, el scroll principal
           permitirá desplazarse para ver todo."""
        # calculamos un ancho objetivo relativo al ancho de la ventana
        target_w = int(self.width() * 0.80)
        if target_w < 480:
            target_w = 480   # mínimo práctico

        if not self.pm_camion.isNull():
            orig_w = self.pm_camion.width()
            orig_h = self.pm_camion.height()
            ratio = (orig_h / orig_w) if orig_w else (self.ref_camion_h / self.ref_camion_w)
            target_h = int(target_w * ratio)
            # asignamos tamaño a la etiqueta (pixmap se escalará por scaledContents=True)
            self.camion_label.setFixedSize(target_w, target_h)
            # opcional: si quieres mantener la imagen en su ratio real y no estirar, puedes usar:
            # self.camion_label.setPixmap(self.pm_camion.scaled(target_w, target_h, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            target_w, target_h = 661, 191
            self.camion_label.setFixedSize(target_w, target_h)

        # overlay sigue el tamaño del label
        cw = self.camion_label.width()
        ch = self.camion_label.height()
        self.overlay.setGeometry(0, 0, cw, ch)

        # calculo de área interior escalada
        sx = cw / self.ref_camion_w
        sy = ch / self.ref_camion_h

        interior_x = int(self.ref_interior.x() * sx)
        interior_y = int(self.ref_interior.y() * sy)
        interior_w = int(self.ref_interior.width() * sx)
        interior_h = int(self.ref_interior.height() * sy)

        pad_x = 8
        pad_y = 3

        usable_w = max(10, interior_w - 2*pad_x)
        usable_h = max(10, interior_h - 2*pad_y)

        # SEPARACIÓN CONTROLADA (horizontal)
        gap_x = 32   # reduce para que entren mejor en tamaños pequeños (ajústalo)
        gap_y = 8

        # tamaño de asiento en base a espacio usable
        seat_w = int((usable_w - (self.cols-1)*gap_x) / self.cols)
        seat_h = int(usable_h / self.rows)
        seat_size = max(28, min(52, min(seat_w, seat_h)))  # límites para que no exploten

        total_seats_width = self.cols * seat_size + (self.cols-1) * gap_x
        start_x = interior_x + pad_x + max(0, (usable_w - total_seats_width)//2)
        start_y = interior_y + pad_y

        # Posicionar cada botón (hijos absolutos del overlay)
        for r in range(1, self.rows+1):
            for c in range(1, self.cols+1):
                btn = self.seat_buttons[(r,c)]
                x = start_x + (c-1) * (seat_size + gap_x)
                y = start_y + (r-1) * (seat_size + gap_y)
                btn.setGeometry(x, y, seat_size, seat_size)

                key = (r,c)
                if key in self.occupied:
                    btn.setEnabled(False)
                    if not self.icon_ocup.isNull():
                        btn.setIcon(QIcon(self.icon_ocup))
                else:
                    if key in self.special_positions and not self.icon_esp.isNull():
                        btn.setIcon(QIcon(self.icon_esp))
                    elif not self.icon_disp.isNull():
                        btn.setIcon(QIcon(self.icon_disp))

                btn.setIconSize(QSize(int(seat_size*0.75), int(seat_size*0.75)))

                if key in self.selected:
                    if key in self.special_positions and not self.icon_esp_sel.isNull():
                        btn.setIcon(QIcon(self.icon_esp_sel))
                    elif not self.icon_sel.isNull():
                        btn.setIcon(QIcon(self.icon_sel))

    # ---------------------------------------
    def on_seat_clicked(self, row, col, btn):
        key = (row, col)
        if key in self.occupied:
            return

        if btn.isChecked():
            self.selected.append(key)
            if key in self.special_positions and not self.icon_esp_sel.isNull():
                btn.setIcon(QIcon(self.icon_esp_sel))
            elif not self.icon_sel.isNull():
                btn.setIcon(QIcon(self.icon_sel))
        else:
            if key in self.selected:
                self.selected.remove(key)
            if key in self.special_positions and not self.icon_esp.isNull():
                btn.setIcon(QIcon(self.icon_esp))
            elif not self.icon_disp.isNull():
                btn.setIcon(QIcon(self.icon_disp))

        if self.selected:
            r, c = self.selected[-1]

            ASIENTOS_POR_FILA = 9

            # c YA empieza desde 1 → no sumamos +1
            asiento_real = (r - 1) * ASIENTOS_POR_FILA + c

            self.info_label.setText(
                f"Fila: {r}   Asiento: {asiento_real}   Seleccionados: {len(self.selected)}"
            )
        else:
            self.info_label.setText("Fila: -   Asiento: -")
    # ---------------------------------------
    def on_accept(self):
        if not self.selected:
            QMessageBox.warning(self, "Sin selección", "Debes seleccionar al menos un asiento.")
            return

        for key in list(self.selected):
            self.occupied.add(key)
            btn = self.seat_buttons[key]
            btn.setEnabled(False)
            if not self.icon_ocup.isNull():
                btn.setIcon(QIcon(self.icon_ocup))

        self.selected.clear()
        self.info_label.setText("Fila: -   Asiento: -")
        # si quieres actualizar labels de info de viaje, hazlo aquí:
        # self.lbl_viaje.setText("Número de viaje: 1234") etc.

    # ---------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # cada vez que cambie el tamaño de la ventana, recalculamos pos y tamaños
        self._update_camion_and_overlay()


# ---------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaAsientos()
    ventana.show()
    sys.exit(app.exec())