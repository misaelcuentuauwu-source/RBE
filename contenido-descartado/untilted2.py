from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox
from PySide6.QtCore import Qt, Signal
from conexion import crear_conexion
from pasajero import VentanaRegistroPasajero
from precio import VentanaPrecio
from untitled import Ui_MainWindow  # UI modernizada

class SeleccionarAsiento(QWidget):
    def __init__(self, id_viaje, taquillero_id=200):
        super().__init__()
        self.id_viaje = id_viaje
        self.taquillero_id = taquillero_id

        # Instancia de la UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Variables de control
        self.asientos_seleccionados = []
        self.botones_asientos = []
        self.boletos_pendientes = []
        self.asiento_index = 0

        # Inicializar asientos
        self.cargar_asientos()

        # Conectar botón de confirmación
        self.ui.btn_confirmar.clicked.connect(self.confirmar_asientos)

    def cargar_asientos(self):
        """
        Carga los asientos desde la base de datos.
        Si no existen asientos para el viaje, los inserta automáticamente.
        """
        db = crear_conexion()
        cursor = db.cursor()

        # Verificar si ya hay asientos para el viaje
        cursor.execute("SELECT COUNT(*) FROM viaje_asiento WHERE viaje = %s", (self.id_viaje,))
        total = cursor.fetchone()[0]

        if total == 0:
            # Insertar asientos automáticamente
            cursor.execute("""
                INSERT INTO viaje_asiento (asiento, viaje, ocupado)
                SELECT a.numero, %s, 0
                FROM asiento a
                WHERE a.autobus = (SELECT autobus FROM viaje WHERE numero = %s)
            """, (self.id_viaje, self.id_viaje))
            db.commit()

        # Obtener todos los asientos del viaje
        cursor.execute("""
            SELECT a.numero, va.ocupado
            FROM viaje_asiento va
            JOIN asiento a ON va.asiento = a.numero
            WHERE va.viaje = %s
            ORDER BY a.numero
        """, (self.id_viaje,))
        asientos = cursor.fetchall()
        db.close()

        # Layout de la UI donde se agregan los botones
        layout_asientos = self.ui.layout_asientos
        columnas = 4

        for i, (num_asiento, ocupado) in enumerate(asientos):
            fila = i // columnas
            col = i % columnas
            etiqueta = f"{fila + 1}{chr(65 + col)}"

            btn = QPushButton(etiqueta)
            btn.setFixedSize(60, 40)
            btn.setProperty("id_asiento", num_asiento)

            if ocupado:
                btn.setStyleSheet("background-color: #ccc; color: #666;")
                btn.setEnabled(False)
            else:
                btn.setStyleSheet("background-color: #4CAF50; color: white;")
                btn.clicked.connect(self.seleccionar_asiento)

            layout_asientos.addWidget(btn, fila, col)
            self.botones_asientos.append(btn)

    def seleccionar_asiento(self):
        """
        Marca o desmarca un asiento al hacer clic.
        """
        btn = self.sender()
        id_asiento = btn.property("id_asiento")

        if id_asiento in self.asientos_seleccionados:
            self.asientos_seleccionados.remove(id_asiento)
            btn.setStyleSheet("background-color: #4CAF50; color: white;")
        else:
            self.asientos_seleccionados.append(id_asiento)
            btn.setStyleSheet("background-color: #0078ff; color: white;")

    def confirmar_asientos(self):
        """
        Inicia el registro de pasajeros para los asientos seleccionados.
        """
        if not self.asientos_seleccionados:
            QMessageBox.warning(self, "Aviso", "Selecciona al menos un asiento.")
            return

        self.asiento_index = 0
        self.boletos_pendientes = []
        self.abrir_registro_para_asiento()

    def abrir_registro_para_asiento(self):
        """
        Abre la ventana de registro de pasajero para el asiento actual.
        """
        asiento_id = self.asientos_seleccionados[self.asiento_index]
        numero_pasajero = self.asiento_index + 1

        self.ventana_registro = VentanaRegistroPasajero(numero_pasajero, asiento_id)
        self.ventana_registro.pasajero_registrado.connect(self.procesar_pasajero)
        self.ventana_registro.show()

    def procesar_pasajero(self, pasajero_id):
        """
        Guarda la información del pasajero registrado y avanza al siguiente asiento.
        """
        asiento_id = self.asientos_seleccionados[self.asiento_index]
        self.boletos_pendientes.append((pasajero_id, asiento_id))

        self.asiento_index += 1
        if self.asiento_index < len(self.asientos_seleccionados):
            self.abrir_registro_para_asiento()
        else:
            # Todos los pasajeros registrados, abrir ventana de precio
            self.ventana_precio = VentanaPrecio(self.id_viaje, self.taquillero_id, self.boletos_pendientes)
            self.ventana_precio.show()
            self.close()
