# ventana_asientosxd.py
# Interfaz DINÁMICA de selección de asientos con PASILLO CENTRAL HORIZONTAL

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QSizePolicy, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt, QSize, QRect, Signal
from PySide6.QtGui import QPixmap, QIcon, QFont
import sys
import os
import math
from conexion import crear_conexion
import recursos_rc

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
    asientos_seleccionados = Signal(list)
    
    def __init__(self, id_viaje, num_pasajeros=1):
        super().__init__()
        self.id_viaje = id_viaje
        self.num_pasajeros = num_pasajeros
        self.setWindowTitle("Seleccionar asientos - Rutas Baja Express")
        self.resize(1200, 760)

        self.pm_logo = load_pixmap_try([":/recursos/logocirculo.png", "logocirculo.png"])
        self.pm_mapa = load_pixmap_try([":/recursos/mapa de Baja Califor.png", "mapa de Baja Califor.png"])
        self.pm_camion = load_pixmap_try([":/recursos/autobusmarco.png", "autobusmarco.png"])
        self.icon_disp = load_pixmap_try([":/recursos/asiento.svg", "asiento.svg"])
        self.icon_sel = load_pixmap_try([":/recursos/asientoseleccionado.svg", "asientoseleccionado.svg"])
        self.icon_ocup = load_pixmap_try([":/recursos/asientoocupado.svg", "asientoocupado.svg"])
        self.icon_esp = load_pixmap_try([":/recursos/asientoespecial.svg", "asientoespecial.svg"])
        self.icon_esp_sel = load_pixmap_try([":/recursos/asientoespecialseleccionado.svg", "asientoespecialseleccionado.svg"])

        self.total_asientos = 0
        self.rows = 0
        self.cols_left = 0
        self.cols_right = 0
        self.special_positions = set()
        self.occupied = set()
        self.selected = []
        self.autobus_numero = None
        
        self.asientos_para_registrar = []
        self.tipos_pasajeros = []
        self.pasajeros_registrados = []
        self.indice_actual = 0
        self.precio_base = 0.0

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        main_container = QWidget()
        scroll.setWidget(main_container)
        self.setCentralWidget(scroll)

        root = QVBoxLayout(main_container)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(10)

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
        lh.addWidget(item_ley("Seleccionado", "#1480c4"))
        lh.addSpacing(70)
        
        self.info_label = QLabel("Asientos disponibles: - | Seleccionados: 0")
        self.info_label.setStyleSheet("font-size:13px; font-weight:bold;")
        lh.addWidget(self.info_label)
        lh.addStretch()
        root.addWidget(legend)

        main_frame = QFrame()
        main_frame.setStyleSheet("background:#0a79b7; border-radius:10px;")
        main_layout = QVBoxLayout(main_frame)
        main_layout.setContentsMargins(12, 12, 12, 12)

        self.camion_label = QLabel()
        self.camion_label.setStyleSheet("background: transparent;")
        if not self.pm_camion.isNull():
            self.camion_label.setPixmap(self.pm_camion)
        self.camion_label.setScaledContents(True)
        self.camion_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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

        info_panel = QFrame()
        info_panel.setStyleSheet("background:white; border-radius:12px; padding:10px;")
        info_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        info_layout = QHBoxLayout(info_panel)
        info_layout.setContentsMargins(10,6,10,6)
        info_layout.setSpacing(20)

        self.lbl_viaje  = QLabel("Viaje: -")
        self.lbl_origen = QLabel("Origen: -")
        self.lbl_dest   = QLabel("Destino: -")
        self.lbl_fecha  = QLabel("Salida: -")
        self.lbl_bus    = QLabel("Bus: -")

        for w in (self.lbl_viaje, self.lbl_origen, self.lbl_dest, self.lbl_fecha, self.lbl_bus):
            w.setStyleSheet("font-size:14px; color:#333;")
            w.setMinimumWidth(140)
            info_layout.addWidget(w)

        root.addWidget(info_panel)

        bottom = QHBoxLayout()
        bottom.addStretch()
        
        self.btn_accept = QPushButton("Continuar al Registro →")
        self.btn_accept.setFixedSize(220, 48)
        self.btn_accept.setStyleSheet("background:#14407C;color:white;border-radius:24px;font-size:15px;font-weight:bold;")
        self.btn_accept.clicked.connect(self.on_accept)

        btn_back = QPushButton("Regresar")
        btn_back.setFixedSize(140, 48)
        btn_back.setStyleSheet("background:#EE733A;color:white;border-radius:24px;font-size:15px;")
        btn_back.clicked.connect(self.close)

        bottom.addWidget(self.btn_accept)
        bottom.addSpacing(12)
        bottom.addWidget(btn_back)
        root.addLayout(bottom)

        self.seat_buttons = {}
        self.ref_camion_w = 600.0
        self.ref_camion_h = 185.0
        self.ref_interior = QRect(78, 18, 503, 148)

        self.cargar_datos_viaje()
        self.cargar_configuracion_asientos()
        self.crear_botones_asientos()
        self.cargar_asientos_ocupados()
        self._update_camion_and_overlay()

    def cargar_datos_viaje(self):
        try:
            conn = crear_conexion()
            if not conn:
                QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos")
                return
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT v.numero AS viaje_num, v.fecHoraSalida, 
                   t_origen.nombre AS origen, t_destino.nombre AS destino,
                   a.numero AS autobus_num, a.placas, m.numasientos, r.precio
            FROM viaje v
            JOIN ruta r ON v.ruta = r.codigo
            JOIN terminal t_origen ON r.origen = t_origen.numero
            JOIN terminal t_destino ON r.destino = t_destino.numero
            LEFT JOIN autobus a ON v.autobus = a.numero
            LEFT JOIN modelo m ON a.modelo = m.numero
            WHERE v.numero = %s
            """
            cursor.execute(query, (self.id_viaje,))
            viaje = cursor.fetchone()
            if viaje:
                self.autobus_numero = viaje['autobus_num']
                self.total_asientos = viaje['numasientos'] or 36
                self.precio_base = float(viaje['precio'])
                
                self.lbl_viaje.setText(f"Viaje: #{viaje['viaje_num']}")
                self.lbl_origen.setText(f"Origen: {viaje['origen']}")
                self.lbl_dest.setText(f"Destino: {viaje['destino']}")
                self.lbl_fecha.setText(f"Salida: {viaje['fecHoraSalida'].strftime('%d/%m/%Y %H:%M')}")
                self.lbl_bus.setText(f"Bus: {viaje['autobus_num']} ({viaje['placas']})")
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos del viaje:\n{e}")
    
    def cargar_configuracion_asientos(self):
        """Configura la distribución de asientos CON PASILLO CENTRAL VERTICAL"""
        # rows = columnas verticales (de arriba hacia abajo)
        # cols = filas de asientos uno al lado del otro
        if self.total_asientos <= 24:
            # 2 asientos arriba del pasillo, 2 abajo
            self.cols_left = 2  # Asientos arriba del pasillo
            self.cols_right = 2  # Asientos abajo del pasillo
            self.rows = math.ceil(self.total_asientos / 4)  # Columnas verticales
        elif self.total_asientos <= 44:
            self.cols_left = 2
            self.cols_right = 2
            self.rows = math.ceil(self.total_asientos / 4)
        else:
            self.cols_left = 2
            self.cols_right = 2
            self.rows = math.ceil(self.total_asientos / 4)
        
        # Asientos especiales (primera columna, cerca del conductor)
        self.special_positions = {('L', 1, 1), ('R', 1, 1)}
    
    def crear_botones_asientos(self):
        """Crea los botones con distribución HORIZONTAL de pasillo central"""
        counter = 1
        
        for r in range(1, self.rows + 1):
            for c in range(1, self.cols_left + 1):
                if counter > self.total_asientos:
                    break
                btn = QPushButton(str(counter), self.overlay)
                btn.setCheckable(True)
                btn.setStyleSheet("border:none; background:transparent;")
                btn.clicked.connect(lambda checked, rr=r, cc=c, num=counter, b=btn: 
                                  self.on_seat_clicked('L', rr, cc, num, b))
                self.seat_buttons[('L', r, c)] = btn
                counter += 1
            
            for c in range(1, self.cols_right + 1):
                if counter > self.total_asientos:
                    break
                btn = QPushButton(str(counter), self.overlay)
                btn.setCheckable(True)
                btn.setStyleSheet("border:none; background:transparent;")
                btn.clicked.connect(lambda checked, rr=r, cc=c, num=counter, b=btn: 
                                  self.on_seat_clicked('R', rr, cc, num, b))
                self.seat_buttons[('R', r, c)] = btn
                counter += 1
    
    def cargar_asientos_ocupados(self):
        """Carga los asientos ocupados desde la BD"""
        try:
            conn = crear_conexion()
            if not conn:
                return
            cursor = conn.cursor(dictionary=True)
            query_ocupados = """
            SELECT va.asiento FROM viaje_asiento va
            WHERE va.viaje = %s AND va.ocupado = TRUE
            """
            cursor.execute(query_ocupados, (self.id_viaje,))
            ocupados = cursor.fetchall()
            
            for row in ocupados:
                num_asiento = row['asiento']
                if num_asiento <= self.total_asientos:
                    asientos_por_fila = self.cols_left + self.cols_right
                    fila = ((num_asiento - 1) // asientos_por_fila) + 1
                    pos_en_fila = ((num_asiento - 1) % asientos_por_fila) + 1
                    
                    if pos_en_fila <= self.cols_left:
                        lado = 'L'
                        col = pos_en_fila
                    else:
                        lado = 'R'
                        col = pos_en_fila - self.cols_left
                    
                    self.occupied.add((lado, fila, col))
            
            disponibles = self.total_asientos - len(ocupados)
            self.info_label.setText(f"Disponibles: {disponibles}/{self.total_asientos} | Seleccionados: 0")
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.warning(self, "Aviso", f"No se pudieron cargar asientos ocupados:\n{e}")

    def _update_camion_and_overlay(self):
        """Actualiza la posición de los asientos VERTICALMENTE con pasillo HORIZONTAL en medio"""
        target_w = int(self.width() * 0.80)
        if target_w < 480:
            target_w = 480
        
        if not self.pm_camion.isNull():
            orig_w = self.pm_camion.width()
            orig_h = self.pm_camion.height()
            ratio = (orig_h / orig_w) if orig_w else (self.ref_camion_h / self.ref_camion_w)
            target_h = int(target_w * ratio)
            self.camion_label.setFixedSize(target_w, target_h)
        else:
            target_w, target_h = 661, 191
            self.camion_label.setFixedSize(target_w, target_h)
        
        cw = self.camion_label.width()
        ch = self.camion_label.height()
        self.overlay.setGeometry(0, 0, cw, ch)
        
        sx = cw / self.ref_camion_w
        sy = ch / self.ref_camion_h
        interior_x = int(self.ref_interior.x() * sx)
        interior_y = int(self.ref_interior.y() * sy)
        interior_w = int(self.ref_interior.width() * sx)
        interior_h = int(self.ref_interior.height() * sy)
        
        pad_x, pad_y = 15, 10
        usable_w = max(10, interior_w - 2*pad_x)
        usable_h = max(10, interior_h - 2*pad_y)
        
        # Espaciado
        gap_col = 8  # Espacio horizontal entre columnas
        gap_row = 6  # Espacio vertical entre asientos de la misma columna
        pasillo_height = 18  # Altura del pasillo HORIZONTAL en medio
        
        # Calcular tamaño de asientos
        seat_w = (usable_w - (self.rows - 1) * gap_col) // self.rows
        
        # Altura disponible para asientos (restando el pasillo horizontal)
        available_height = usable_h - pasillo_height
        total_rows_vertical = self.cols_left + self.cols_right
        seat_h = (available_height - (total_rows_vertical - 1) * gap_row) // total_rows_vertical
        
        seat_size = max(28, min(42, min(seat_w, seat_h)))
        
        # Posición inicial (arriba a la izquierda)
        start_x = interior_x + pad_x
        start_y = interior_y + pad_y
        
        # Posicionar asientos COLUMNA POR COLUMNA (de izquierda a derecha)
        for col_num in range(1, self.rows + 1):
            current_x = start_x + (col_num - 1) * (seat_size + gap_col)
            
            # PARTE SUPERIOR (arriba del pasillo)
            current_y = start_y
            for row_num in range(1, self.cols_left + 1):
                key = ('L', col_num, row_num)
                if key in self.seat_buttons:
                    btn = self.seat_buttons[key]
                    btn.setGeometry(current_x, current_y, seat_size, seat_size)
                    
                    if key in self.occupied:
                        btn.setEnabled(False)
                        if not self.icon_ocup.isNull():
                            btn.setIcon(QIcon(self.icon_ocup))
                    else:
                        btn.setEnabled(True)
                        if key in self.special_positions and not self.icon_esp.isNull():
                            btn.setIcon(QIcon(self.icon_esp))
                        elif not self.icon_disp.isNull():
                            btn.setIcon(QIcon(self.icon_disp))
                    
                    btn.setIconSize(QSize(int(seat_size*0.7), int(seat_size*0.7)))
                    
                    if key in [(k[0], k[1], k[2]) for k, _ in self.selected]:
                        if key in self.special_positions and not self.icon_esp_sel.isNull():
                            btn.setIcon(QIcon(self.icon_esp_sel))
                        elif not self.icon_sel.isNull():
                            btn.setIcon(QIcon(self.icon_sel))
                    
                    current_y += seat_size + gap_row
            
            # PASILLO HORIZONTAL (saltar el espacio)
            current_y += pasillo_height
            
            # PARTE INFERIOR (abajo del pasillo)
            for row_num in range(1, self.cols_right + 1):
                key = ('R', col_num, row_num)
                if key in self.seat_buttons:
                    btn = self.seat_buttons[key]
                    btn.setGeometry(current_x, current_y, seat_size, seat_size)
                    
                    if key in self.occupied:
                        btn.setEnabled(False)
                        if not self.icon_ocup.isNull():
                            btn.setIcon(QIcon(self.icon_ocup))
                    else:
                        btn.setEnabled(True)
                        if key in self.special_positions and not self.icon_esp.isNull():
                            btn.setIcon(QIcon(self.icon_esp))
                        elif not self.icon_disp.isNull():
                            btn.setIcon(QIcon(self.icon_disp))
                    
                    btn.setIconSize(QSize(int(seat_size*0.7), int(seat_size*0.7)))
                    
                    if key in [(k[0], k[1], k[2]) for k, _ in self.selected]:
                        if key in self.special_positions and not self.icon_esp_sel.isNull():
                            btn.setIcon(QIcon(self.icon_esp_sel))
                        elif not self.icon_sel.isNull():
                            btn.setIcon(QIcon(self.icon_sel))
                    
                    current_y += seat_size + gap_row

    def on_seat_clicked(self, lado, row, col, num_asiento, btn):
        """Maneja el click en un asiento"""
        key = (lado, row, col)
        if key in self.occupied:
            return
        
        if btn.isChecked():
            self.selected.append((key, num_asiento))
            if key in self.special_positions and not self.icon_esp_sel.isNull():
                btn.setIcon(QIcon(self.icon_esp_sel))
            elif not self.icon_sel.isNull():
                btn.setIcon(QIcon(self.icon_sel))
        else:
            self.selected = [(k, n) for k, n in self.selected if k != key]
            if key in self.special_positions and not self.icon_esp.isNull():
                btn.setIcon(QIcon(self.icon_esp))
            elif not self.icon_disp.isNull():
                btn.setIcon(QIcon(self.icon_disp))
        
        disponibles = self.total_asientos - len(self.occupied)
        self.info_label.setText(f"Disponibles: {disponibles}/{self.total_asientos} | Seleccionados: {len(self.selected)}")

    def on_accept(self):
        """Inicia el proceso de registro de pasajeros"""
        if not self.selected:
            QMessageBox.warning(self, "Sin selección", "Debes seleccionar al menos un asiento.")
            return
        
        self.asientos_para_registrar = [num for _, num in self.selected]
        
        respuesta = QMessageBox.question(
            self, "Confirmar selección",
            f"Has seleccionado {len(self.asientos_para_registrar)} asiento(s): {self.asientos_para_registrar}\n\n"
            f"¿Deseas continuar al registro de pasajeros?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            self.tipos_pasajeros = []
            self.pasajeros_registrados = []
            self.indice_actual = 0
            self.abrir_ventana_tipo_pasajero()

    def abrir_ventana_tipo_pasajero(self):
        """Abre ventana para seleccionar tipo de pasajero"""
        from ventana_tipo_pasajero import VentanaTipoPasajero
        
        if self.indice_actual >= len(self.asientos_para_registrar):
            self.abrir_ventana_pago()
            return
        
        asiento_actual = self.asientos_para_registrar[self.indice_actual]
        
        self.ventana_tipo = VentanaTipoPasajero(
            numero_pasajero=self.indice_actual + 1,
            asiento_id=asiento_actual,
            total_pasajeros=len(self.asientos_para_registrar)
        )
        
        self.ventana_tipo.tipo_seleccionado.connect(self.on_tipo_seleccionado)
        self.ventana_tipo.show()
    
    def on_tipo_seleccionado(self, tipo_num):
        """Guarda el tipo y abre ventana de registro"""
        self.tipos_pasajeros.append(tipo_num)
        self.abrir_ventana_registro_pasajero()
    
    def abrir_ventana_registro_pasajero(self):
        """Abre ventana de registro de datos del pasajero"""
        from ventana_registro_pasajero import VentanaRegistroPasajero
        
        asiento_actual = self.asientos_para_registrar[self.indice_actual]
        tipo_actual = self.tipos_pasajeros[self.indice_actual]
        
        self.ventana_registro = VentanaRegistroPasajero(
            numero_pasajero=self.indice_actual + 1,
            asiento_id=asiento_actual,
            total_pasajeros=len(self.asientos_para_registrar)
        )
        
        self.ventana_registro.pasajero_registrado.connect(
            lambda pid: self.on_pasajero_registrado(pid, asiento_actual, tipo_actual)
        )
        self.ventana_registro.show()
    
    def on_pasajero_registrado(self, pasajero_id, asiento_id, tipo_pasajero):
        """Guarda info del pasajero y continúa con el siguiente"""
        self.pasajeros_registrados.append({
            'pasajero_id': pasajero_id,
            'asiento_id': asiento_id,
            'tipo_pasajero': tipo_pasajero
        })
        
        self.indice_actual += 1
        self.abrir_ventana_tipo_pasajero()
    
    def abrir_ventana_pago(self):
        """Abre ventana de pago con resumen"""
        from ventana_pago import VentanaPago
        
        self.ventana_pago = VentanaPago(
            pasajeros_info=self.pasajeros_registrados,
            id_viaje=self.id_viaje,
            precio_base=self.precio_base
        )
        
        self.ventana_pago.pago_confirmado.connect(self.finalizar_compra)
        self.ventana_pago.show()
    
    def finalizar_compra(self):
        """Marca asientos como ocupados y cierra"""
        try:
            conn = crear_conexion()
            if not conn:
                return
            
            cursor = conn.cursor()
            for asiento_num in self.asientos_para_registrar:
                update_query = """
                UPDATE viaje_asiento SET ocupado = TRUE 
                WHERE viaje = %s AND asiento = %s
                """
                cursor.execute(update_query, (self.id_viaje, asiento_num))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            QMessageBox.information(
                self, "¡Compra exitosa!", 
                f"Se completó la compra de {len(self.pasajeros_registrados)} boletos.\n\n"
                "Gracias por tu preferencia."
            )
            
            self.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al finalizar:\n{e}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_camion_and_overlay()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaAsientos(id_viaje=1, num_pasajeros=2)
    ventana.show()
    sys.exit(app.exec())