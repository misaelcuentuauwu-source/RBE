# kpi_calculos.py
# Ventana de KPIs con tarjetas tipo dashboard (Top 5 integrado)

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QDateEdit, QComboBox, QPushButton, QGridLayout,
    QSizePolicy
)
from PySide6.QtCore import Qt, QDate
from datetime import date, timedelta
from conexion import crear_conexion


class KPIWindowGenerales(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KPI Dashboard - RBE")
        self.setMinimumSize(0, 0)   # permite que se adapte
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.db = crear_conexion()

        # ======= CONTENEDOR PRINCIPAL =======
        main = QVBoxLayout(self)
        main.setContentsMargins(40, 20, 40, 20)
        main.setSpacing(20)

        # ======= TÍTULO =======
        titulo = QLabel("Dashboard — KPIs")
        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1A2B4C;
        """)
        main.addWidget(titulo)

        # ============================================================
        # FILTROS
        # ============================================================
        filtro_row = QHBoxLayout()
        filtro_row.setSpacing(15)

        # Rango: Día / Semana / Mes
        self.rango = QComboBox()
        self.rango.addItems(["Día", "Semana", "Mes"])
        self.rango.currentIndexChanged.connect(self.update_filter_ui)

        # --- Filtro día ---
        self.fecha_dia = QDateEdit()
        self.fecha_dia.setCalendarPopup(True)
        self.fecha_dia.setDate(QDate.currentDate())

        # --- Filtro mes ---
        self.fecha_mes = QComboBox()
        self.fecha_mes.addItems([
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        self.fecha_mes.hide()

        actualizar = QPushButton("Actualizar")
        actualizar.clicked.connect(self.update_metrics)
        actualizar.setStyleSheet("""
            QPushButton {
                background: #FF7F3F;
                color: white;
                border-radius: 10px;
                padding: 8px 18px;
                font-size: 15px;
            }
            QPushButton:hover {
                background: #ff8f55;
            }
        """)

        filtro_row.addWidget(QLabel("Rango:"))
        filtro_row.addWidget(self.rango)
        filtro_row.addWidget(self.fecha_dia)
        filtro_row.addWidget(self.fecha_mes)
        filtro_row.addStretch()
        filtro_row.addWidget(actualizar)

        main.addLayout(filtro_row)

        # ======= GRID DE TARJETAS =======
        grid = QGridLayout()
        grid.setSpacing(25)

        self.card_boletos = self.create_card("Boletos vendidos")
        self.card_conductor = self.create_card("Conductores - Top 5")
        self.card_autobus = self.create_card("Autobuses - Top 5")
        self.card_ciudad_visitada = self.create_card("Ciudades destino - Top 5")
        self.card_ciudad_origen = self.create_card("Ciudades origen - Top 5")

        grid.addWidget(self.card_boletos, 0, 0)
        grid.addWidget(self.card_conductor, 0, 1)
        grid.addWidget(self.card_autobus, 0, 2)
        grid.addWidget(self.card_ciudad_visitada, 1, 0)
        grid.addWidget(self.card_ciudad_origen, 1, 1)

        # distribuir columnas (ayuda al grid a expandirse uniformemente)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)

        main.addLayout(grid)

        # Inicializar UI y métricas
        self.update_filter_ui()
        # opcional: actualizar métricas al abrir
        # self.update_metrics()

    # ============================================================
    # Cambiar filtros según rango seleccionado
    # ============================================================
    def update_filter_ui(self):
        rango = self.rango.currentText()

        if rango == "Día":
            self.fecha_dia.show()
            self.fecha_mes.hide()

        elif rango == "Semana":
            self.fecha_dia.hide()
            self.fecha_mes.hide()

        elif rango == "Mes":
            self.fecha_dia.hide()
            self.fecha_mes.show()

    # ============================================================
    # Crear tarjeta KPI (ahora lista para Top 5)
    # ============================================================
    def create_card(self, titulo):
        frame = QFrame()
        frame.setMinimumSize(260, 150)  # tamaño mínimo
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        frame.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border-radius: 16px;
                border: 2px solid #E6E6E6;
                border-left: 8px solid #FF7F3F;  /* naranja RBE */
            }
        """)

        lay = QVBoxLayout(frame)
        lay.setContentsMargins(18, 18, 18, 18)
        lay.setSpacing(8)

        title = QLabel(titulo)
        title.setStyleSheet("""
            font-size: 15px;
            color: #1A2B4C;  /* azul corporativo */
            font-weight: 600;
        """)

        lay.addWidget(title)

        # Contenedor para múltiples valores (Top 5)
        values_layout = QVBoxLayout()
        values_layout.setSpacing(4)

        # Guardamos el layout en el frame para actualizar después
        frame.values_layout = values_layout

        lay.addLayout(values_layout)
        lay.addStretch()
        return frame

    # ============================================================
    # Ejecutar consulta (único resultado)
    # ============================================================
    def query(self, sql, params=None):
        cur = self.db.cursor(dictionary=True)
        cur.execute(sql, params or ())
        return cur.fetchone()

    # ============================================================
    # Ejecutar consulta (varios resultados)
    # ============================================================
    def query_all(self, sql, params=None):
        cur = self.db.cursor(dictionary=True)
        cur.execute(sql, params or ())
        rows = cur.fetchall()
        # fetchall devuelve lista de dicts cuando dictionary=True
        return rows or []

    # ============================================================
    # Obtener rango de fechas
    # ============================================================
    def get_date_range(self):
        rango = self.rango.currentText()

        if rango == "Día":
            d = self.fecha_dia.date().toPython()
            return d, d

        elif rango == "Semana":
            hoy = date.today()
            inicio = hoy - timedelta(days=hoy.weekday())
            fin = inicio + timedelta(days=6)
            return inicio, fin

        elif rango == "Mes":
            mes = self.fecha_mes.currentIndex() + 1
            año = date.today().year
            inicio = date(año, mes, 1)
            fin = date(año, mes, 28) + timedelta(days=4)
            fin = fin.replace(day=1) - timedelta(days=1)
            return inicio, fin

    # ============================================================
    # Mostrar Top5 dentro de una tarjeta
    # label_field: campo con el texto (nombre, ciudad, etc.)
    # count_field: campo con el valor numérico (total)
    # ============================================================
    def set_top5(self, frame, data, label_field, count_field='total'):
        # limpiar contenido anterior
        while frame.values_layout.count():
            it = frame.values_layout.takeAt(0)
            w = it.widget()
            if w:
                w.deleteLater()

        if not data:
            lbl = QLabel("Sin datos")
            lbl.setStyleSheet("font-size: 14px; color: #555;")
            lbl.setWordWrap(True)
            frame.values_layout.addWidget(lbl)
            return

        for idx, row in enumerate(data):
            label = row.get(label_field) or str(row.get(count_field, ''))
            count = row.get(count_field, None)

            # construir texto: "1. Nombre — 123"
            text = f"{idx+1}. {label}"
            if count is not None:
                text = f"{text} — {count}"

            lbl = QLabel(text)
            lbl.setWordWrap(True)  # <-- evitar desbordamiento
            lbl.setFixedHeight(26) # <-- mantiene altura uniforme

            # estilos por posición, más compactos
            if idx == 0:
                lbl.setStyleSheet("font-size: 18px; font-weight: 700; color: #000;")
            elif idx <= 2:
                lbl.setStyleSheet("font-size: 15px; font-weight: 600; color: #222;")
            else:
                lbl.setStyleSheet("font-size: 13px; color: #555;")

            frame.values_layout.addWidget(lbl)

    # ============================================================
    # Actualizar KPIs (ahora con Top 5)
    # ============================================================
    def update_metrics(self):
        desde, hasta = self.get_date_range()

        # 1) BOLETOS VENDIDOS — Top destinos por boletos
        b_lista = self.query_all("""
            SELECT ci.nombre AS ciudad, COUNT(*) AS total
            FROM ticket t
            JOIN viaje v ON v.numero = t.viaje
            JOIN ruta r ON r.codigo = v.ruta
            JOIN terminal ter ON ter.numero = r.destino
            JOIN ciudad ci ON ci.clave = ter.ciudad
            WHERE DATE(v.fecHoraSalida) BETWEEN %s AND %s
            GROUP BY ci.clave
            ORDER BY total DESC
            LIMIT 5
        """, (desde, hasta))
        self.set_top5(self.card_boletos, b_lista, "ciudad", "total")

        # 2) CONDUCTORES — Top 5 por número de viajes
        c_lista = self.query_all("""
            SELECT CONCAT(c.conNombre, ' ', c.conPrimerApell) AS nombre, COUNT(*) AS total
            FROM viaje v
            JOIN conductor c ON c.registro = v.conductor
            WHERE DATE(v.fecHoraSalida) BETWEEN %s AND %s
            GROUP BY v.conductor
            ORDER BY total DESC
            LIMIT 5
        """, (desde, hasta))
        self.set_top5(self.card_conductor, c_lista, "nombre", "total")

        # 3) AUTOBUSES — Top 5 por número de viajes
        a_lista = self.query_all("""
            SELECT a.numero AS autobus_num, COUNT(*) AS total
            FROM viaje v
            JOIN autobus a ON a.numero = v.autobus
            WHERE DATE(v.fecHoraSalida) BETWEEN %s AND %s
            GROUP BY a.numero
            ORDER BY total DESC
            LIMIT 5
        """, (desde, hasta))
        self.set_top5(self.card_autobus, a_lista, "autobus_num", "total")

        # 4) CIUDADES DESTINO — Top 5
        ci_lista = self.query_all("""
            SELECT ci.nombre AS nombre, COUNT(*) AS total
            FROM viaje v
            JOIN ruta r ON r.codigo = v.ruta
            JOIN terminal t ON t.numero = r.destino
            JOIN ciudad ci ON ci.clave = t.ciudad
            WHERE DATE(v.fecHoraSalida) BETWEEN %s AND %s
            GROUP BY ci.clave
            ORDER BY total DESC
            LIMIT 5
        """, (desde, hasta))
        self.set_top5(self.card_ciudad_visitada, ci_lista, "nombre", "total")

        # 5) CIUDADES ORIGEN — Top 5
        cv_lista = self.query_all("""
            SELECT ci.nombre AS nombre, COUNT(*) AS total
            FROM viaje v
            JOIN ruta r ON r.codigo = v.ruta
            JOIN terminal t ON t.numero = r.origen
            JOIN ciudad ci ON ci.clave = t.ciudad
            WHERE DATE(v.fecHoraSalida) BETWEEN %s AND %s
            GROUP BY ci.clave
            ORDER BY total DESC
            LIMIT 5
        """, (desde, hasta))
        self.set_top5(self.card_ciudad_origen, cv_lista, "nombre", "total")


# ---------------------------------------------------------------
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = KPIWindowGenerales()
    win.show()
    sys.exit(app.exec())