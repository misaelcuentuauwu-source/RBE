# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)
import recursos_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget_13 = QWidget(self.centralwidget)
        self.widget_13.setObjectName(u"widget_13")
        self.widget_13.setGeometry(QRect(0, 0, 741, 541))
        self.widget_13.setStyleSheet(u"background-color: rgb(20, 128, 196);")
        self.frame_3 = QFrame(self.widget_13)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(-10, 0, 741, 81))
        self.frame_3.setStyleSheet(u"background-color: rgb(238, 115, 58);")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.label_5 = QLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(90, 10, 231, 51))
        self.label_5.setStyleSheet(u"color: rgb(255,255,255);\n"
"font: 18pt \"Segoe UI\";\n"
"font: 600 20pt \"Segoe UI\";")
        self.label_17 = QLabel(self.frame_3)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(20, 10, 61, 61))
        self.label_17.setStyleSheet(u"image: url(:/recursos/logocirculo.png);")
        self.label_19 = QLabel(self.frame_3)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(600, -10, 91, 111))
        self.label_19.setStyleSheet(u"image: url(:/recursos/mapa de Baja Califor.png);")
        self.frame_2 = QFrame(self.widget_13)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(10, 100, 681, 91))
        self.frame_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius:25px;")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.label_20 = QLabel(self.frame_2)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(510, 50, 21, 21))
        self.label_20.setStyleSheet(u"image: url(:/recursos/icon5.svg);")
        self.label_21 = QLabel(self.frame_2)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(540, 50, 121, 20))
        self.label_21.setStyleSheet(u"color: rgb(229, 229, 229);\n"
"font: 16pt \"Segoe UI\";\n"
"font: 600 12pt \"Segoe UI\";")
        self.label_22 = QLabel(self.frame_2)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(400, 50, 101, 20))
        self.label_22.setStyleSheet(u"color: rgb(229, 229, 229);\n"
"font: 16pt \"Segoe UI\";\n"
"font: 600 12pt \"Segoe UI\";")
        self.label_23 = QLabel(self.frame_2)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setGeometry(QRect(370, 50, 21, 21))
        self.label_23.setStyleSheet(u"image: url(:/recursos/icon3.svg);")
        self.label_24 = QLabel(self.frame_2)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(260, 50, 21, 21))
        self.label_24.setStyleSheet(u"image: url(:/recursos/icon2.svg);")
        self.label_25 = QLabel(self.frame_2)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(290, 50, 71, 20))
        self.label_25.setStyleSheet(u"color: rgb(229, 229, 229);\n"
"font: 16pt \"Segoe UI\";\n"
"font: 600 12pt \"Segoe UI\";")
        self.label_26 = QLabel(self.frame_2)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(QRect(160, 50, 81, 20))
        self.label_26.setStyleSheet(u"color: rgb(229, 229, 229);\n"
"font: 16pt \"Segoe UI\";\n"
"font: 600 12pt \"Segoe UI\";")
        self.label_27 = QLabel(self.frame_2)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setGeometry(QRect(130, 50, 21, 21))
        self.label_27.setStyleSheet(u"image: url(:/recursos/icon.svg);")
        self.label_28 = QLabel(self.frame_2)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QRect(50, 50, 71, 20))
        self.label_28.setStyleSheet(u"color: rgb(229, 229, 229);\n"
"font: 16pt \"Segoe UI\";\n"
"font: 600 12pt \"Segoe UI\";")
        self.label_29 = QLabel(self.frame_2)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setGeometry(QRect(20, 50, 21, 21))
        self.label_29.setStyleSheet(u"image: url(:/recursos/icon4.svg);")
        self.label_30 = QLabel(self.frame_2)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setGeometry(QRect(20, 10, 191, 31))
        self.label_30.setStyleSheet(u"font: 14pt \"Segoe UI\";")
        self.widget_12 = QWidget(self.widget_13)
        self.widget_12.setObjectName(u"widget_12")
        self.widget_12.setGeometry(QRect(20, 230, 661, 191))
        self.widget_12.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.widget_2 = QWidget(self.widget_13)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(20, 230, 661, 191))
        self.widget_2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.pushButton_54 = QPushButton(self.widget_13)
        self.pushButton_54.setObjectName(u"pushButton_54")
        self.pushButton_54.setGeometry(QRect(500, 450, 81, 31))
        self.pushButton_54.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(20, 100, 156);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.pushButton_5 = QPushButton(self.widget_13)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(590, 450, 81, 31))
        self.pushButton_5.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(238, 115, 58);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.widget_2.raise_()
        self.widget_12.raise_()
        self.frame_3.raise_()
        self.frame_2.raise_()
        self.pushButton_54.raise_()
        self.pushButton_5.raise_()
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 190, 681, 271))
        self.widget.setStyleSheet(u"image: url(:/recursos/autobusmarco.png);")
        self.pushButton_62 = QPushButton(self.widget)
        self.pushButton_62.setObjectName(u"pushButton_62")
        self.pushButton_62.setGeometry(QRect(440, 190, 34, 34))
        self.pushButton_62.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_62.setCheckable(True)
        self.pushButton_29 = QPushButton(self.widget)
        self.pushButton_29.setObjectName(u"pushButton_29")
        self.pushButton_29.setGeometry(QRect(260, 190, 34, 34))
        self.pushButton_29.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_29.setCheckable(True)
        self.pushButton_32 = QPushButton(self.widget)
        self.pushButton_32.setObjectName(u"pushButton_32")
        self.pushButton_32.setGeometry(QRect(440, 150, 34, 34))
        self.pushButton_32.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_32.setCheckable(True)
        self.pushButton_33 = QPushButton(self.widget)
        self.pushButton_33.setObjectName(u"pushButton_33")
        self.pushButton_33.setGeometry(QRect(380, 150, 34, 34))
        self.pushButton_33.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_33.setCheckable(True)
        self.pushButton_34 = QPushButton(self.widget)
        self.pushButton_34.setObjectName(u"pushButton_34")
        self.pushButton_34.setGeometry(QRect(260, 150, 34, 34))
        self.pushButton_34.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_34.setCheckable(True)
        self.pushButton_22 = QPushButton(self.widget)
        self.pushButton_22.setObjectName(u"pushButton_22")
        self.pushButton_22.setGeometry(QRect(560, 50, 34, 34))
        self.pushButton_22.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_22.setCheckable(True)
        self.pushButton_77 = QPushButton(self.widget)
        self.pushButton_77.setObjectName(u"pushButton_77")
        self.pushButton_77.setGeometry(QRect(140, 90, 34, 34))
        self.pushButton_77.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asientoespecial.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientoespecialcursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoespecialseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoespecialseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_77.setCheckable(True)
        self.pushButton_35 = QPushButton(self.widget)
        self.pushButton_35.setObjectName(u"pushButton_35")
        self.pushButton_35.setGeometry(QRect(320, 50, 34, 34))
        self.pushButton_35.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_35.setCheckable(True)
        self.pushButton_64 = QPushButton(self.widget)
        self.pushButton_64.setObjectName(u"pushButton_64")
        self.pushButton_64.setGeometry(QRect(380, 190, 34, 34))
        self.pushButton_64.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_64.setCheckable(True)
        self.pushButton_71 = QPushButton(self.widget)
        self.pushButton_71.setObjectName(u"pushButton_71")
        self.pushButton_71.setGeometry(QRect(620, 150, 34, 34))
        self.pushButton_71.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_71.setCheckable(True)
        self.pushButton_72 = QPushButton(self.widget)
        self.pushButton_72.setObjectName(u"pushButton_72")
        self.pushButton_72.setGeometry(QRect(320, 190, 34, 34))
        self.pushButton_72.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_72.setCheckable(True)
        self.pushButton_78 = QPushButton(self.widget)
        self.pushButton_78.setObjectName(u"pushButton_78")
        self.pushButton_78.setGeometry(QRect(500, 150, 34, 34))
        self.pushButton_78.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_78.setCheckable(True)
        self.pushButton_36 = QPushButton(self.widget)
        self.pushButton_36.setObjectName(u"pushButton_36")
        self.pushButton_36.setGeometry(QRect(500, 50, 34, 34))
        self.pushButton_36.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_36.setCheckable(True)
        self.pushButton_79 = QPushButton(self.widget)
        self.pushButton_79.setObjectName(u"pushButton_79")
        self.pushButton_79.setGeometry(QRect(500, 190, 34, 34))
        self.pushButton_79.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_79.setCheckable(True)
        self.pushButton_37 = QPushButton(self.widget)
        self.pushButton_37.setObjectName(u"pushButton_37")
        self.pushButton_37.setGeometry(QRect(380, 50, 34, 34))
        self.pushButton_37.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_37.setCheckable(True)
        self.pushButton_38 = QPushButton(self.widget)
        self.pushButton_38.setObjectName(u"pushButton_38")
        self.pushButton_38.setGeometry(QRect(500, 90, 34, 34))
        self.pushButton_38.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_38.setCheckable(True)
        self.pushButton_80 = QPushButton(self.widget)
        self.pushButton_80.setObjectName(u"pushButton_80")
        self.pushButton_80.setGeometry(QRect(140, 150, 34, 34))
        self.pushButton_80.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asientoespecial.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientoespecialcursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoespecialseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoespecialseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_80.setCheckable(True)
        self.pushButton_39 = QPushButton(self.widget)
        self.pushButton_39.setObjectName(u"pushButton_39")
        self.pushButton_39.setGeometry(QRect(560, 90, 34, 34))
        self.pushButton_39.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_39.setCheckable(True)
        self.pushButton_40 = QPushButton(self.widget)
        self.pushButton_40.setObjectName(u"pushButton_40")
        self.pushButton_40.setGeometry(QRect(260, 50, 34, 34))
        self.pushButton_40.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_40.setCheckable(True)
        self.pushButton_41 = QPushButton(self.widget)
        self.pushButton_41.setObjectName(u"pushButton_41")
        self.pushButton_41.setGeometry(QRect(440, 90, 34, 34))
        self.pushButton_41.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_41.setCheckable(True)
        self.pushButton_42 = QPushButton(self.widget)
        self.pushButton_42.setObjectName(u"pushButton_42")
        self.pushButton_42.setGeometry(QRect(320, 90, 34, 34))
        self.pushButton_42.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_42.setCheckable(True)
        self.pushButton_81 = QPushButton(self.widget)
        self.pushButton_81.setObjectName(u"pushButton_81")
        self.pushButton_81.setGeometry(QRect(560, 190, 34, 34))
        self.pushButton_81.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_81.setCheckable(True)
        self.pushButton_43 = QPushButton(self.widget)
        self.pushButton_43.setObjectName(u"pushButton_43")
        self.pushButton_43.setGeometry(QRect(440, 50, 34, 34))
        self.pushButton_43.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_43.setCheckable(True)
        self.pushButton_44 = QPushButton(self.widget)
        self.pushButton_44.setObjectName(u"pushButton_44")
        self.pushButton_44.setGeometry(QRect(620, 90, 34, 34))
        self.pushButton_44.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_44.setCheckable(True)
        self.pushButton_45 = QPushButton(self.widget)
        self.pushButton_45.setObjectName(u"pushButton_45")
        self.pushButton_45.setGeometry(QRect(260, 90, 34, 34))
        self.pushButton_45.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_45.setCheckable(True)
        self.pushButton_46 = QPushButton(self.widget)
        self.pushButton_46.setObjectName(u"pushButton_46")
        self.pushButton_46.setGeometry(QRect(380, 90, 34, 34))
        self.pushButton_46.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_46.setCheckable(True)
        self.pushButton_47 = QPushButton(self.widget)
        self.pushButton_47.setObjectName(u"pushButton_47")
        self.pushButton_47.setGeometry(QRect(560, 150, 34, 34))
        self.pushButton_47.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_47.setCheckable(True)
        self.pushButton_82 = QPushButton(self.widget)
        self.pushButton_82.setObjectName(u"pushButton_82")
        self.pushButton_82.setGeometry(QRect(320, 150, 34, 34))
        self.pushButton_82.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_82.setCheckable(True)
        self.pushButton_48 = QPushButton(self.widget)
        self.pushButton_48.setObjectName(u"pushButton_48")
        self.pushButton_48.setGeometry(QRect(620, 190, 34, 34))
        self.pushButton_48.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_48.setCheckable(True)
        self.pushButton_49 = QPushButton(self.widget)
        self.pushButton_49.setObjectName(u"pushButton_49")
        self.pushButton_49.setGeometry(QRect(620, 50, 34, 34))
        self.pushButton_49.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_49.setCheckable(True)
        self.pushButton_83 = QPushButton(self.widget)
        self.pushButton_83.setObjectName(u"pushButton_83")
        self.pushButton_83.setGeometry(QRect(200, 90, 34, 34))
        self.pushButton_83.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_83.setCheckable(True)
        self.pushButton_84 = QPushButton(self.widget)
        self.pushButton_84.setObjectName(u"pushButton_84")
        self.pushButton_84.setGeometry(QRect(200, 150, 34, 34))
        self.pushButton_84.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_84.setCheckable(True)
        self.pushButton_50 = QPushButton(self.widget)
        self.pushButton_50.setObjectName(u"pushButton_50")
        self.pushButton_50.setGeometry(QRect(140, 50, 34, 34))
        self.pushButton_50.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_50.setCheckable(True)
        self.pushButton_51 = QPushButton(self.widget)
        self.pushButton_51.setObjectName(u"pushButton_51")
        self.pushButton_51.setGeometry(QRect(200, 50, 34, 34))
        self.pushButton_51.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_51.setCheckable(True)
        self.pushButton_52 = QPushButton(self.widget)
        self.pushButton_52.setObjectName(u"pushButton_52")
        self.pushButton_52.setGeometry(QRect(200, 190, 34, 34))
        self.pushButton_52.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_52.setCheckable(True)
        self.pushButton_53 = QPushButton(self.widget)
        self.pushButton_53.setObjectName(u"pushButton_53")
        self.pushButton_53.setGeometry(QRect(140, 190, 34, 34))
        self.pushButton_53.setStyleSheet(u"QPushButton {\n"
"    image: url(:/recursos/asiento.svg);\n"
"    qproperty-iconSize: 64px 64px;\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    image: url(:/recursos/asientocursor.svg);\n"
"}\n"
"QPushButton:pressed {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"QPushButton:checked {\n"
"    image: url(:/recursos/asientoseleccionado.svg);\n"
"}\n"
"self.boton.setDisabled(True)\n"
"QPushButton:disabled {\n"
"    image: url(:/recursos/asientoocupado.svg);\n"
"}")
        self.pushButton_53.setCheckable(True)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Rutas Baja Express", None))
        self.label_17.setText("")
        self.label_19.setText("")
        self.label_20.setText("")
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Asiento especial", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Seleccionado", None))
        self.label_23.setText("")
        self.label_24.setText("")
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Seleccion", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Disponible", None))
        self.label_27.setText("")
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Ocupado", None))
        self.label_29.setText("")
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Selecci\u00f3n de asientos", None))
        self.pushButton_54.setText(QCoreApplication.translate("MainWindow", u"Aceptar", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Regresar", None))
        self.pushButton_62.setText(QCoreApplication.translate("MainWindow", u"29", None))
        self.pushButton_29.setText(QCoreApplication.translate("MainWindow", u"23", None))
        self.pushButton_32.setText(QCoreApplication.translate("MainWindow", u"30", None))
        self.pushButton_33.setText(QCoreApplication.translate("MainWindow", u"28", None))
        self.pushButton_34.setText(QCoreApplication.translate("MainWindow", u"24", None))
        self.pushButton_22.setText(QCoreApplication.translate("MainWindow", u"16", None))
        self.pushButton_77.setText(QCoreApplication.translate("MainWindow", u"       1", None))
        self.pushButton_35.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.pushButton_64.setText(QCoreApplication.translate("MainWindow", u"27", None))
        self.pushButton_71.setText(QCoreApplication.translate("MainWindow", u"36", None))
        self.pushButton_72.setText(QCoreApplication.translate("MainWindow", u"25", None))
        self.pushButton_78.setText(QCoreApplication.translate("MainWindow", u"32", None))
        self.pushButton_36.setText(QCoreApplication.translate("MainWindow", u"14", None))
        self.pushButton_79.setText(QCoreApplication.translate("MainWindow", u"31", None))
        self.pushButton_37.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.pushButton_38.setText(QCoreApplication.translate("MainWindow", u"13", None))
        self.pushButton_80.setText(QCoreApplication.translate("MainWindow", u"      20", None))
        self.pushButton_39.setText(QCoreApplication.translate("MainWindow", u"15", None))
        self.pushButton_40.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.pushButton_41.setText(QCoreApplication.translate("MainWindow", u"11", None))
        self.pushButton_42.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.pushButton_81.setText(QCoreApplication.translate("MainWindow", u"33", None))
        self.pushButton_43.setText(QCoreApplication.translate("MainWindow", u"12", None))
        self.pushButton_44.setText(QCoreApplication.translate("MainWindow", u"17", None))
        self.pushButton_45.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.pushButton_46.setText(QCoreApplication.translate("MainWindow", u"9", None))
        self.pushButton_47.setText(QCoreApplication.translate("MainWindow", u"34", None))
        self.pushButton_82.setText(QCoreApplication.translate("MainWindow", u"26", None))
        self.pushButton_48.setText(QCoreApplication.translate("MainWindow", u"35", None))
        self.pushButton_49.setText(QCoreApplication.translate("MainWindow", u"18", None))
        self.pushButton_83.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.pushButton_84.setText(QCoreApplication.translate("MainWindow", u"22", None))
        self.pushButton_50.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.pushButton_51.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.pushButton_52.setText(QCoreApplication.translate("MainWindow", u"21", None))
        self.pushButton_53.setText(QCoreApplication.translate("MainWindow", u"19", None))
    # retranslateUi

