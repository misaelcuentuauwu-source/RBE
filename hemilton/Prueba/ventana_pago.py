# ventana_pago.py
# Ventana de pago con conexión a BD

from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QComboBox, QLineEdit, QSizePolicy, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap
from conexion import crear_conexion
# Al inicio de ventana_pago.py, agregar:
from ventana_generar_boletos import VentanaGenerarBoletos
import recursos_rc


def crear_imagen_r(path, max_w, max_h):
    lbl = QLabel()
    lbl.setAlignment(Qt.AlignCenter)
    lbl.original_pixmap = QPixmap(path)
    lbl.max_w = max_w
    lbl.max_h = max_h
    lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return lbl


class VentanaPago(QWidget):
    # Señal que se emite cuando el pago es confirmado
    pago_confirmado = Signal()
    
    def __init__(self, pasajeros_info=None, id_viaje=None, precio_base=0.0):
        super().__init__()
        
        self.pasajeros_info = pasajeros_info or []
        self.id_viaje = id_viaje
        self.precio_base = precio_base
        self.taquillero_id = 1  # Por ahora usamos ID fijo, deberías obtenerlo del login
        
        self.setWindowTitle("Pago")
        self.resize(1100, 760)

        # ======================================
        # LAYOUT PRINCIPAL
        # ======================================
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # ======================================
        # PANEL IZQUIERDO
        # ======================================
        panel_izq = QWidget()
        panel_izq.setStyleSheet("background: white;")
        layout_principal.addWidget(panel_izq, 3)

        layout_izq = QVBoxLayout(panel_izq)
        layout_izq.setAlignment(Qt.AlignCenter)

        self.img = crear_imagen_r(":/recursos/Cartoon-style illust.png", 450, 450)
        self.logo = crear_imagen_r(":/recursos/Convierte el logo de.png", 350, 350)

        layout_izq.addWidget(self.img)
        layout_izq.addWidget(self.logo)
        layout_izq.addStretch()

        # ======================================
        # PANEL DERECHO con SCROLL
        # ======================================
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: #0074B7; border: none;")
        layout_principal.addWidget(scroll, 4)

        contenedor_der = QWidget()
        scroll.setWidget(contenedor_der)

        layout_der = QVBoxLayout(contenedor_der)
        layout_der.setAlignment(Qt.AlignTop)

        # ======================================
        # TARJETA
        # ======================================
        tarjeta = QFrame()
        tarjeta.setStyleSheet("""
            background: #2A9BE7;
            border-radius: 25px;
        """)
        tarjeta.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout_tarjeta = QVBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(40, 20, 40, 30)
        layout_tarjeta.setSpacing(18)

        layout_der.addWidget(tarjeta, alignment=Qt.AlignCenter)

        # ======================================
        # ICONO Y TEXTOS
        # ======================================
        self.icono = crear_imagen_r(":/recursos/logocirculo.png", 120, 120)

        titulo = QLabel("Pago")
        titulo.setFont(QFont("Arial", 32, QFont.Bold))
        titulo.setStyleSheet("color: white;")

        subtitulo = QLabel("Resumen de compra")
        subtitulo.setStyleSheet("color: #E9E9E9; font-size: 16px;")

        layout_tarjeta.addWidget(self.icono, alignment=Qt.AlignCenter)
        layout_tarjeta.addWidget(titulo, alignment=Qt.AlignCenter)
        layout_tarjeta.addWidget(subtitulo, alignment=Qt.AlignCenter)

        # ======================================
        # TARJETAS DE INFORMACIÓN
        # ======================================
        def crear_info(nombre, valor):
            cont = QFrame()
            cont.setStyleSheet("""
                background: white;
                border-radius: 15px;
            """)
            cont.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            lay = QVBoxLayout(cont)
            lay.setContentsMargins(14, 10, 14, 10)

            lbl1 = QLabel(nombre)
            lbl1.setStyleSheet("color: #555; font-size: 14px;")

            lbl2 = QLabel(valor)
            lbl2.setFont(QFont("Arial", 18, QFont.Bold))
            lbl2.setStyleSheet("color: black;")

            lay.addWidget(lbl1)
            lay.addWidget(lbl2)

            return cont, lbl2

        self.info_boletos, self.lbl_boletos = crear_info("Cantidad de boletos", "0")
        self.info_total, self.lbl_total = crear_info("Total de compra", "$0.00")

        fila = QHBoxLayout()
        fila.addWidget(self.info_boletos)
        fila.addWidget(self.info_total)
        layout_tarjeta.addLayout(fila)

        # ======================================
        # BOTÓN VER DETALLE
        # ======================================
        self.btn_detalle = QPushButton("Ver detalle")
        self.btn_detalle.setStyleSheet("""
            QPushButton {
                background: white;
                padding: 10px;
                border-radius: 15px;
                font-size: 16px;
                color: black;
            }
            QPushButton:hover {
                background: #f0f0f0;
            }
        """)
        self.btn_detalle.clicked.connect(self.mostrar_detalle)
        layout_tarjeta.addWidget(self.btn_detalle)

        # ======================================
        # MÉTODO DE PAGO
        # ======================================
        self.metodo_pago = QComboBox()
        self.cargar_metodos_pago()
        
        self.metodo_pago.setStyleSheet("""
            QComboBox {
                background: white;
                padding: 10px;
                border-radius: 12px;
                font-size: 16px;
                border: 2px solid #cccccc;
                color: black;
            }
            QComboBox:hover {
                border: 2px solid #2A9BE7;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                background: white;
                color: black;
                selection-background-color: #2A9BE7;
                selection-color: white;
                border-radius: 8px;
                padding: 6px;
            }
        """)

        layout_tarjeta.addWidget(self.metodo_pago)

        # ======================================
        # ÁREA DINÁMICA
        # ======================================
        self.area_dinamica = QVBoxLayout()
        layout_tarjeta.addLayout(self.area_dinamica)

        self.metodo_pago.currentTextChanged.connect(self.actualizar_area_pago)

        # ======================================
        # BOTONES
        # ======================================
        botones = QHBoxLayout()

        self.btn_confirmar = QPushButton("Confirmar Pago")
        self.btn_confirmar.setStyleSheet("""
            background: #004C90;
            color: white;
            border-radius: 15px;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
        """)
        self.btn_confirmar.clicked.connect(self.confirmar_pago)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("""
            background: #FF7A00;
            color: white;
            border-radius: 15px;
            padding: 12px;
            font-size: 16px;
        """)
        btn_cancelar.clicked.connect(self.close)

        botones.addWidget(self.btn_confirmar)
        botones.addWidget(btn_cancelar)
        layout_tarjeta.addLayout(botones)

        # Calcular y mostrar totales
        self.calcular_totales()
        self.actualizar_area_pago(self.metodo_pago.currentText())

    def cargar_metodos_pago(self):
        """Carga métodos de pago desde BD"""
        try:
            conn = crear_conexion()
            if not conn:
                return
            
            cursor = conn.cursor(dictionary=True)
            query = "SELECT numero, nombre FROM tipo_pago ORDER BY numero"
            cursor.execute(query)
            metodos = cursor.fetchall()
            
            self.metodos_disponibles = {}
            for metodo in metodos:
                nombre = metodo['nombre']
                id_metodo = metodo['numero']
                self.metodos_disponibles[nombre] = id_metodo
                self.metodo_pago.addItem(nombre)
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            QMessageBox.warning(self, "Aviso", f"Error al cargar métodos de pago:\n{e}")

    def calcular_totales(self):
        """Calcula el total considerando descuentos"""
        try:
            conn = crear_conexion()
            if not conn:
                return
            
            cursor = conn.cursor(dictionary=True)
            total = 0.0
            
            for info in self.pasajeros_info:
                tipo_id = info['tipo_pasajero']
                query = "SELECT descuento FROM tipo_pasajero WHERE num = %s"
                cursor.execute(query, (tipo_id,))
                resultado = cursor.fetchone()
                
                if resultado:
                    descuento = resultado['descuento']
                    precio_con_desc = self.precio_base * (1 - descuento / 100.0)
                    total += precio_con_desc
            
            cursor.close()
            conn.close()
            
            self.total_pagar = total
            self.lbl_boletos.setText(str(len(self.pasajeros_info)))
            self.lbl_total.setText(f"${total:.2f} MXN")
            
        except Exception as e:
            QMessageBox.warning(self, "Aviso", f"Error al calcular totales:\n{e}")

    def mostrar_detalle(self):
        """Muestra el detalle de la compra"""
        try:
            conn = crear_conexion()
            if not conn:
                return
            
            cursor = conn.cursor(dictionary=True)
            detalle = f"DETALLE DE COMPRA\n{'='*40}\n\n"
            
            for i, info in enumerate(self.pasajeros_info, 1):
                # Obtener info del pasajero
                query_pax = "SELECT paNombre, paPrimerApell FROM pasajero WHERE num = %s"
                cursor.execute(query_pax, (info['pasajero_id'],))
                pax = cursor.fetchone()
                
                # Obtener tipo y descuento
                query_tipo = "SELECT descripcion, descuento FROM tipo_pasajero WHERE num = %s"
                cursor.execute(query_tipo, (info['tipo_pasajero'],))
                tipo = cursor.fetchone()
                
                if pax and tipo:
                    nombre = f"{pax['paNombre']} {pax['paPrimerApell']}"
                    tipo_desc = tipo['descripcion']
                    descuento = tipo['descuento']
                    precio = self.precio_base * (1 - descuento / 100.0)
                    
                    detalle += f"Pasajero {i}: {nombre}\n"
                    detalle += f"  Asiento: #{info['asiento_id']}\n"
                    detalle += f"  Tipo: {tipo_desc} (-{descuento}%)\n"
                    detalle += f"  Precio: ${precio:.2f}\n\n"
            
            detalle += f"{'='*40}\n"
            detalle += f"TOTAL: ${self.total_pagar:.2f} MXN"
            
            cursor.close()
            conn.close()
            
            QMessageBox.information(self, "Detalle de compra", detalle)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al mostrar detalle:\n{e}")

    def actualizar_area_pago(self, metodo):
        """Actualiza el área según el método de pago"""
        while self.area_dinamica.count():
            item = self.area_dinamica.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if metodo == "Efectivo":
            total = QLabel(f"Total: ${self.total_pagar:.2f}")
            total.setStyleSheet("color: white; font-size: 18px;")

            self.recibido = QLineEdit()
            self.recibido.setPlaceholderText("Total recibido")
            self.recibido.setStyleSheet("""
                background: white;
                padding: 10px;
                border-radius: 15px;
                color: black;
            """)
            self.recibido.textChanged.connect(self.calcular_cambio)

            self.cambio = QLabel("Cambio: $0.00")
            self.cambio.setStyleSheet("color: white; font-size: 18px;")

            self.area_dinamica.addWidget(total)
            self.area_dinamica.addWidget(self.recibido)
            self.area_dinamica.addWidget(self.cambio)

        else:  # Tarjeta
            for txt in ["Número de tarjeta", "Mes (MM)", "Año (YY)", "CVV"]:
                entrada = QLineEdit()
                entrada.setPlaceholderText(txt)
                entrada.setStyleSheet("""
                    background: white;
                    padding: 10px;
                    border-radius: 15px;
                    color: black;
                """)
                self.area_dinamica.addWidget(entrada)

    def calcular_cambio(self):
        """Calcula el cambio en efectivo"""
        try:
            recibido = float(self.recibido.text())
            cambio = recibido - self.total_pagar
            self.cambio.setText(f"Cambio: ${cambio:.2f}")
        except:
            self.cambio.setText("Cambio: $0.00")

    def confirmar_pago(self):
        """Guarda pago, tickets y marca asientos como ocupados"""
        metodo_texto = self.metodo_pago.currentText()
        
        if metodo_texto not in self.metodos_disponibles:
            QMessageBox.warning(self, "Error", "Método de pago no válido")
            return
        
        tipo_pago_id = self.metodos_disponibles[metodo_texto]
        
        # Validar efectivo
        if metodo_texto == "Efectivo":
            try:
                recibido = float(self.recibido.text())
                if recibido < self.total_pagar:
                    QMessageBox.warning(self, "Error", "El monto recibido es insuficiente")
                    return
            except:
                QMessageBox.warning(self, "Error", "Ingresa el monto recibido")
                return
        
        try:
            conn = crear_conexion()
            if not conn:
                QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos")
                return
            
            cursor = conn.cursor()
            
            # 1. Crear registro de pago
            query_pago = """
            INSERT INTO pago (fechapago, monto, tipo, vendedor)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_pago, (
                datetime.now(),
                self.total_pagar,
                tipo_pago_id,
                self.taquillero_id
            ))
            
            pago_id = cursor.lastrowid
            
            # 2. Crear tickets para cada pasajero
            for info in self.pasajeros_info:
                # Obtener descuento
                cursor.execute("SELECT descuento FROM tipo_pasajero WHERE num = %s", (info['tipo_pasajero'],))
                desc_result = cursor.fetchone()
                descuento = desc_result[0] if desc_result else 0
                
                precio_ticket = self.precio_base * (1 - descuento / 100.0)
                
                query_ticket = """
                INSERT INTO ticket (precio, fechaEmision, asiento, viaje, pasajero, tipopasajero, pago)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_ticket, (
                    precio_ticket,
                    datetime.now(),
                    info['asiento_id'],
                    self.id_viaje,
                    info['pasajero_id'],
                    info['tipo_pasajero'],
                    pago_id
                ))
            
            # 3. Marcar asientos como ocupados (CON FIX) ⭐
            for info in self.pasajeros_info:
                # Primero verificar si existe el registro
                check_query = """
                SELECT asiento FROM viaje_asiento 
                WHERE viaje = %s AND asiento = %s
                """
                cursor.execute(check_query, (self.id_viaje, info['asiento_id']))
                existe = cursor.fetchone()
                
                if existe:
                    # Si existe, actualizar
                    update_query = """
                    UPDATE viaje_asiento 
                    SET ocupado = TRUE 
                    WHERE viaje = %s AND asiento = %s
                    """
                    cursor.execute(update_query, (self.id_viaje, info['asiento_id']))
                else:
                    # Si no existe, insertar
                    insert_query = """
                    INSERT INTO viaje_asiento (viaje, asiento, ocupado)
                    VALUES (%s, %s, TRUE)
                    """
                    cursor.execute(insert_query, (self.id_viaje, info['asiento_id']))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # Mensaje de éxito
            QMessageBox.information(
                self, "¡Pago exitoso!",
                f"Se procesó el pago correctamente.\n\n"
                f"Total: ${self.total_pagar:.2f}\n"
                f"Boletos: {len(self.pasajeros_info)}\n"
                f"Método: {metodo_texto}\n\n"
                f"A continuación podrás personalizar y exportar tus boletos."
            )
            
            # ⭐ ABRIR VENTANA DE GENERACIÓN DE BOLETOS
            self.ventana_boletos = VentanaGenerarBoletos(
                pasajeros_info=self.pasajeros_info,
                id_viaje=self.id_viaje
            )
            self.ventana_boletos.show()
            
            # Emitir señal y cerrar ventana de pago
            self.pago_confirmado.emit()
            self.close()
            
        except Exception as e:
            if conn:
                conn.rollback()
            QMessageBox.critical(self, "Error", f"Error al procesar pago:\n{e}")

    def resizeEvent(self, event):
        for lbl in [self.img, self.logo, self.icono]:
            pix = lbl.original_pixmap
            if not pix.isNull():
                lbl.setPixmap(
                    pix.scaled(
                        min(lbl.width(), lbl.max_w),
                        min(lbl.height(), lbl.max_h),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )
        return super().resizeEvent(event)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    
    # Datos de prueba
    pasajeros_prueba = [
        {'pasajero_id': 1, 'asiento_id': 12, 'tipo_pasajero': 1},
        {'pasajero_id': 2, 'asiento_id': 13, 'tipo_pasajero': 2}
    ]
    
    v = VentanaPago(pasajeros_info=pasajeros_prueba, id_viaje=1, precio_base=250.0)
    v.show()
    sys.exit(app.exec())