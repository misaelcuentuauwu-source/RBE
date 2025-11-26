#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rutas Baja Express - UI responsiva con PySide6 (todo en un archivo)
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QScrollArea,
    QSpinBox, QDateEdit, QCalendarWidget
)
from PySide6.QtCore import Qt, QRect, QSize, QPoint, QDate
from PySide6.QtGui import QFont, QPixmap

# Importar recursos qrc compilados
import recursos_rc  

# -----------------------
# FlowLayout (wrapping)
# -----------------------
class FlowLayout(__import__('PySide6.QtWidgets', fromlist=['QLayout']).QLayout):
    def __init__(self, parent=None, margin=0, spacing=24):
        super().__init__(parent)
        self._items = []
        self.setSpacing(spacing)
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item):
        self._items.append(item)

    def addWidget(self, widget):
        self.addChildWidget(widget)
        self.addItem(widget)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        from PySide6.QtWidgets import QWidgetItem
        if 0 <= index < len(self._items):
            it = self._items[index]
            if isinstance(it, QWidget):
                return QWidgetItem(it)
            return it
        return None

    def takeAt(self, index):
        from PySide6.QtWidgets import QWidgetItem
        if 0 <= index < len(self._items):
            it = self._items.pop(index)
            if isinstance(it, QWidget):
                return QWidgetItem(it)
            return it
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            hint = item.sizeHint() if hasattr(item, "sizeHint") else item.widget().sizeHint()
            size = size.expandedTo(hint)
        l, t, r, b = self.getContentsMargins()
        size += QSize(l + r, t + b)
        return size

    def doLayout(self, rect, test):
        x = rect.x()
        y = rect.y()
        lineH = 0
        left, top, right, bottom = self.getContentsMargins()
        x += left
        y += top
        maxW = rect.width() - (left + right)

        for item in self._items:
            widget = item if isinstance(item, QWidget) else item.widget()
            hint = widget.sizeHint()
            w, h = hint.width(), hint.height()

            if x + w > rect.x() + maxW and x > rect.x() + left:
                x = rect.x() + left
                y += lineH + self.spacing()
                lineH = 0

            if not test:
                widget.setGeometry(QRect(QPoint(x, y), QSize(w, h)))

            x += w + self.spacing()
            lineH = max(lineH, h)

        return y + lineH + bottom


# -----------------------
# Main UI
# -----------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rutas Baja Express")
        self.resize(1100, 760)

        # ======== ESTILO GLOBAL PARA INPUTS ==========
        self.setStyleSheet("""
        QComboBox, QDateEdit, QSpinBox {
            background: white;
            border: 2px solid #cccccc;
            border-radius: 10px;
            padding: 6px 10px;
            font-size: 14px;
            min-width: 150px;
        }

        QComboBox::drop-down,
        QDateEdit::drop-down {
            border: none;
            width: 28px;
        }

        QComboBox::down-arrow {
            image: url(:/icons/down.svg);
            width: 14px;
            height: 14px;
        }

        QDateEdit::down-arrow {
            image: url(:/icons/calendar.svg);
            width: 14px;
            height: 14px;
        }

        QSpinBox::up-button, 
        QSpinBox::down-button {
            width: 20px;
            border: none;
        }

        QSpinBox::up-arrow {
            image: url(:/icons/up.svg);
        }

        QSpinBox::down-arrow {
            image: url(:/icons/down.svg);
        }

        QComboBox:hover, QDateEdit:hover, QSpinBox:hover {
            border: 2px solid #aaaaaa;
        }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # ---------- HEADER ----------
        header = QFrame()
        header.setStyleSheet("background:#E86A1E;border-radius:12px;")
        h_header = QHBoxLayout(header)
        h_header.setContentsMargins(16, 10, 16, 10)

        # Logo bus
        bus = QLabel()
        bus.setFixedSize(72, 72)
        pixmap = QPixmap(":/recursos/logocirculo.png")
        pixmap = pixmap.scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        bus.setPixmap(pixmap)
        h_header.addWidget(bus)

        title = QLabel("Rutas Baja Express")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setStyleSheet("color:white;")
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        h_header.addWidget(title)

        # Imagen mapa
        map_img = QLabel()
        map_img.setFixedSize(72, 72)
        pixmap_map = QPixmap(":/recursos/mapa de Baja Califor.png")
        pixmap_map = pixmap_map.scaled(92, 92, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        map_img.setPixmap(pixmap_map)
        h_header.addWidget(map_img)

        root.addWidget(header)

        # ---------- BLUE WRAPPER ----------
        blue = QFrame()
        blue.setStyleSheet("background:#0a79b7;border-radius:12px;")
        blue_l = QVBoxLayout(blue)
        blue_l.setContentsMargins(12, 12, 12, 12)
        blue_l.setSpacing(14)

        # ---------- BUSCADOR ----------
        buscador = QFrame()
        buscador.setStyleSheet("background:white;border-radius:10px;")
        busc_l = QHBoxLayout(buscador)
        busc_l.setContentsMargins(30, 12, 30, 12)

        flow_container = QWidget()
        flow = FlowLayout(flow_container, margin=0, spacing=4)

        # ===================================================
        #   PLACEHOLDER INTERNO PARA COMBOBOX (Tipo A)
        # ===================================================
        def setupComboPlaceholder(combo, placeholder):
            combo.insertItem(0, placeholder)
            combo.setCurrentIndex(0)

            combo.view().setRowHidden(0, True)

            combo.setStyleSheet("""
                QComboBox {
                    color: #888;
                }
            """)

            def update(i):
                if i == 0:
                    combo.setStyleSheet("QComboBox { color:#888; }")
                else:
                    combo.setStyleSheet("QComboBox { color:black; }")

            combo.currentIndexChanged.connect(update)

        # ORIGEN
        cb_origin = QComboBox()
        cb_origin.addItems(["Tijuana"])
        setupComboPlaceholder(cb_origin, "Origen")

        # DESTINO
        cb_dest = QComboBox()
        cb_dest.addItems(["San Quintín", "Ensenada", "La Paz", "Ensenada", "Mexicali"])
        setupComboPlaceholder(cb_dest, "Destino")

        # ===================================================
        #   ** NUEVO Y MEJORADO QDATEEDIT **
        # ===================================================

        # ------------------------
        # QDATEEDIT CON PLACEHOLDER
        # ------------------------
        date = QDateEdit()
        date.setCalendarPopup(True)
        date.setDate(QDate.currentDate())
        date.setDisplayFormat("dd/MM/yyyy")   # Formato visible

        # -- FECHA REAL (se mantiene guardada)
        self.fecha_real = QDate.currentDate()

        # -- PLACEHOLDER SUPERPUESTO --
        placeholder = QLabel("Fecha", date)
        placeholder.setStyleSheet("color:#888; padding-left:10px;font-size:14px;")
        placeholder.move(6, 4)  # Ajustar posición
        placeholder.resize(170, 30) 
        placeholder.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Mostrar placeholder inicialmente
        placeholder.show()
        date.dateChanged.connect(lambda *_: placeholder.hide())
        # Cuando el usuario abre el calendario → marcar que está en selección
        def abrir_calendario():
            placeholder.hide()

        date.calendarWidget().activated.connect(lambda d: seleccionar_fecha(d))

        def seleccionar_fecha(d):
            date.setDate(d)        # Mostrar la fecha elegida
            placeholder.hide()     # Ocultar placeholder
            self.fecha_real = d    # Guardar nueva fecha

        date.lineEdit().textChanged.connect(
            lambda txt: placeholder.setVisible(txt.strip() == "")
        )


        # -----------------------------
        #  🔥 MODIFICACIÓN QUE PEDISTE  
        #  (QUITA NÚMEROS DE SEMANA)
        # -----------------------------
        calendar = QCalendarWidget()
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        # Estilo moderno
        calendar.setStyleSheet("""
            QCalendarWidget QWidget {
                background-color: #ffffff;
                font-size: 15px;
            }
            QCalendarWidget QToolButton {
                color: #333;
                background-color: #f5f5f5;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #e0e0e0;
            }
            QCalendarWidget QSpinBox {
                font-size: 14px;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #0a79b7;
                selection-color: white;
                font-size: 14px;
            }
        """)

        date.setCalendarWidget(calendar)

        # ===================================================
        #   COMBO PASAJEROS
        # ===================================================
        cb_pasajeros = QComboBox()
        cb_pasajeros.addItems([str(i) for i in range(1, 11)])
        setupComboPlaceholder(cb_pasajeros, "Pasajeros")

        # Agregar widgets al flow
        for w in (cb_origin, cb_dest, date, cb_pasajeros):
            wrapper = QWidget()
            wrap_layout = QVBoxLayout(wrapper)
            wrap_layout.setContentsMargins(12, 9, 12, 0)
            wrap_layout.addWidget(w)
            flow.addWidget(wrapper)

        busc_l.addWidget(flow_container, stretch=1)

        btn = QPushButton("➜")
        btn.setFixedSize(56, 56)
        btn.setStyleSheet("background:#E86A1E;color:white;border-radius:12px;font-size:20px;")
        busc_l.addWidget(btn)

        blue_l.addWidget(buscador)

        # ---------- Viajes ----------
        lbl = QLabel("Viajes disponibles:")
        lbl.setFont(QFont("Segoe UI", 20, QFont.Bold))
        lbl.setStyleSheet("color:white;")
        blue_l.addWidget(lbl)

        # ---------- Scroll viajes ----------
        card = QFrame()
        card.setStyleSheet("background:white;border-radius:10px;")
        card_l = QVBoxLayout(card)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameStyle(QFrame.NoFrame)

        sw = QWidget()
        sw_l = QVBoxLayout(sw)

        for _ in range(3):
            sw_l.addWidget(self._make_trip())
        sw_l.addStretch()

        scroll.setWidget(sw)
        card_l.addWidget(scroll)

        blue_l.addWidget(card, stretch=1)
        root.addWidget(blue, stretch=1)

        # ---------- Back Button ----------
        back = QPushButton("Regresar")
        back.setFixedHeight(44)
        back.setStyleSheet("background:#E86A1E;color:white;border-radius:12px;")
        back.clicked.connect(self.close)
        root.addWidget(back, alignment=Qt.AlignLeft)

    # Trip card
    def _make_trip(self):
        card = QFrame()
        card.setStyleSheet("background:white;border-radius:10px;")
        layout = QHBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)

        img = QLabel()
        img.setFixedSize(140, 90)
        pixmap = QPixmap(":/recursos/camiona.png")
        pixmap = pixmap.scaled(140, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img.setPixmap(pixmap)
        layout.addWidget(img)

        center = QVBoxLayout()
        top = QHBoxLayout()

        h1 = QLabel("11:00AM")
        h1.setFont(QFont("Segoe UI", 28, QFont.Bold))
        h2 = QLabel("11:00AM")
        h2.setFont(QFont("Segoe UI", 28, QFont.Bold))

        top.addWidget(h1)
        top.addWidget(QLabel("●───────────────────────●"))
        top.addWidget(h2)
        center.addLayout(top)

        bottom = QHBoxLayout()
        bottom.addWidget(QLabel("Tijuana"))
        bottom.addStretch()
        bottom.addWidget(QLabel(" 10 horas 30 min"))
        bottom.addStretch()
        bottom.addWidget(QLabel("San Quintín"))
        center.addLayout(bottom)

        layout.addLayout(center, stretch=1)

        price_l = QVBoxLayout()
        price = QLabel("$1500 MXN")
        price.setFont(QFont("Segoe UI", 16, QFont.Bold))
        price.setStyleSheet("color:#E86A1E;")
        price_l.addWidget(price)

        btn_go = QPushButton("➜")
        btn_go.setFixedSize(56, 56)
        btn_go.setStyleSheet("background:#E86A1E;color:white;border-radius:28px;")
        price_l.addWidget(btn_go)

        layout.addLayout(price_l)
        return card


# -----------------------
# Run
# -----------------------
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()