# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'menuinicial.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFrame,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QStackedWidget, QWidget)
import recursos_rc

class Ui_loginWindow(object):
    def setupUi(self, loginWindow):
        if not loginWindow.objectName():
            loginWindow.setObjectName(u"loginWindow")
        loginWindow.resize(700, 500)
        loginWindow.setMinimumSize(QSize(700, 500))
        loginWindow.setMaximumSize(QSize(700, 500))
        loginWindow.setStyleSheet(u"QWidget#centralwidget{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(20, 128, 196, 255), stop:1 rgba(238, 115, 58, 255));}")
        self.centralwidget = QWidget(loginWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.menuinicial = QStackedWidget(self.centralwidget)
        self.menuinicial.setObjectName(u"menuinicial")
        self.menuinicial.setGeometry(QRect(0, 0, 701, 511))
        self.menuinicial.setStyleSheet(u"QWidget#centralwidget{background-color: rgb(20, 128, 196);}\n"
"background-color: rgb(255, 255, 255);")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(320, 80, 311, 321))
        self.label.setStyleSheet(u"image: url(:/recursos/logo.png);")
        self.frame = QFrame(self.page)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, -10, 231, 522))
        self.frame.setStyleSheet(u"background-color: rgb(238, 115, 58);")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 140, 201, 51))
        self.label_2.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 18pt \"Segoe UI\";\n"
"font: 600 18pt \"Segoe UI\";")
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(60, 20, 131, 121))
        self.label_5.setStyleSheet(u"image: url(:/recursos/logocirculo.png);")
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(20, 210, 201, 41))
        self.pushButton.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"font: 600 10pt \"Segoe UI\";\n"
"color: rgb(238, 115, 58);")
        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(20, 270, 201, 41))
        self.pushButton_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"font: 600 10pt \"Segoe UI\";\n"
"color: rgb(238, 115, 58);")
        self.pushButton_3 = QPushButton(self.frame)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(20, 330, 201, 41))
        self.pushButton_3.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"font: 600 10pt \"Segoe UI\";\n"
"color: rgb(238, 115, 58);")
        self.pushButton_4 = QPushButton(self.frame)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(30, 440, 181, 31))
        self.pushButton_4.setStyleSheet(u"background-color: rgb(20, 128, 196);\n"
"font: 600 10pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.pushButton_40 = QPushButton(self.frame)
        self.pushButton_40.setObjectName(u"pushButton_40")
        self.pushButton_40.setGeometry(QRect(20, 390, 201, 41))
        self.pushButton_40.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"font: 600 10pt \"Segoe UI\";\n"
"color: rgb(238, 115, 58);")
        self.widget_14 = QWidget(self.page)
        self.widget_14.setObjectName(u"widget_14")
        self.widget_14.setGeometry(QRect(229, -10, 481, 521))
        self.widget_14.setStyleSheet(u"background-color: rgb(234, 234, 234);")
        self.menuinicial.addWidget(self.page)
        self.widget_14.raise_()
        self.label.raise_()
        self.frame.raise_()
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.frame_5 = QFrame(self.page_3)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setGeometry(QRect(10, 230, 671, 261))
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.pushButton_33 = QPushButton(self.frame_5)
        self.pushButton_33.setObjectName(u"pushButton_33")
        self.pushButton_33.setGeometry(QRect(580, 220, 81, 31))
        self.pushButton_33.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(238, 115, 58);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.label_50 = QLabel(self.frame_5)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setGeometry(QRect(10, 20, 101, 71))
        self.label_50.setStyleSheet(u"image: url(:/recursos/camiona.png);")
        self.label_51 = QLabel(self.frame_5)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setGeometry(QRect(130, 15, 211, 71))
        self.label_51.setStyleSheet(u"font: 600 28pt \"Segoe UI\";")
        self.label_52 = QLabel(self.frame_5)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setGeometry(QRect(190, 10, 49, 16))
        self.label_53 = QLabel(self.frame_5)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setGeometry(QRect(270, 85, 51, 21))
        self.label_53.setStyleSheet(u"image: url(:/recursos/clock.svg);")
        self.label_54 = QLabel(self.frame_5)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setGeometry(QRect(310, 85, 91, 21))
        self.label_55 = QLabel(self.frame_5)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setGeometry(QRect(410, 15, 141, 71))
        self.label_55.setStyleSheet(u"font: 600 28pt \"Segoe UI\";")
        self.pushButton_41 = QPushButton(self.frame_5)
        self.pushButton_41.setObjectName(u"pushButton_41")
        self.pushButton_41.setGeometry(QRect(580, 40, 50, 50))
        self.pushButton_41.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(238, 115, 58);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:25px;\n"
"image: url(:/recursos/flecha.png);")
        self.label_56 = QLabel(self.frame_5)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setGeometry(QRect(460, 10, 49, 16))
        self.frame_7 = QFrame(self.frame_5)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setGeometry(QRect(280, 15, 120, 80))
        self.frame_7.setStyleSheet(u"color: rgb(238, 115, 58);")
        self.frame_7.setFrameShape(QFrame.Shape.HLine)
        self.frame_7.setFrameShadow(QFrame.Shadow.Plain)
        self.label_57 = QLabel(self.frame_5)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setGeometry(QRect(280, 51, 8, 8))
        self.label_57.setStyleSheet(u"image: url(:/recursos/icon.svg);")
        self.label_58 = QLabel(self.frame_5)
        self.label_58.setObjectName(u"label_58")
        self.label_58.setGeometry(QRect(396, 51, 8, 8))
        self.label_58.setStyleSheet(u"image: url(:/recursos/icon.svg);")
        self.label_59 = QLabel(self.frame_5)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setGeometry(QRect(560, 15, 101, 16))
        self.label_59.setStyleSheet(u"font: 600 14pt \"Segoe UI\";\n"
"color: rgb(238, 115, 58);")
        self.label_60 = QLabel(self.frame_5)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setGeometry(QRect(190, 90, 49, 16))
        self.label_61 = QLabel(self.frame_5)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setGeometry(QRect(450, 90, 71, 16))
        self.label_19 = QLabel(self.page_3)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(20, 180, 181, 51))
        self.label_19.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 16pt \"Segoe UI\";\n"
"font: 600 16pt \"Segoe UI\";")
        self.frame_4 = QFrame(self.page_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(10, 100, 681, 81))
        self.frame_4.setStyleSheet(u"QWidget#frame_2{\n"
"border-radius:15px;\n"
"background-color: rgb(255, 255, 255);}\n"
"")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.pushButton_29 = QPushButton(self.frame_4)
        self.pushButton_29.setObjectName(u"pushButton_29")
        self.pushButton_29.setGeometry(QRect(610, 20, 61, 41))
        self.pushButton_29.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(238, 115, 58);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;\n"
"image: url(:/recursos/flecha.png);")
        self.comboBox = QComboBox(self.frame_4)
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(9, 20, 161, 41))
        self.comboBox.setEditable(False)
        self.comboBox_2 = QComboBox(self.frame_4)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(180, 20, 161, 41))
        self.comboBox_2.setEditable(False)
        self.fecha = QDateEdit(self.frame_4)
        self.fecha.setObjectName(u"fecha")
        self.fecha.setGeometry(QRect(350, 20, 121, 41))
        self.fecha.setReadOnly(False)
        self.fecha.setDateTime(QDateTime(QDate(2000, 1, 1), QTime(0, 0, 0)))
        self.fecha.setCalendarPopup(True)
        self.comboBox_3 = QComboBox(self.frame_4)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setGeometry(QRect(480, 20, 121, 41))
        self.comboBox_3.setEditable(False)
        self.frame_6 = QFrame(self.page_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setGeometry(QRect(0, 0, 721, 81))
        self.frame_6.setStyleSheet(u"background-color: rgb(238, 115, 58);")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.label_20 = QLabel(self.frame_6)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(90, 10, 231, 51))
        self.label_20.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 18pt \"Segoe UI\";\n"
"font: 600 20pt \"Segoe UI\";")
        self.label_21 = QLabel(self.frame_6)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(20, 10, 61, 61))
        self.label_21.setStyleSheet(u"image: url(:/recursos/logocirculo.png);")
        self.label_22 = QLabel(self.frame_6)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(540, -10, 151, 111))
        self.label_22.setStyleSheet(u"image: url(:/recursos/mapa de Baja Califor.png);")
        self.widget_2 = QWidget(self.page_3)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(-11, -20, 721, 541))
        self.widget_2.setStyleSheet(u"background-color: rgb(20, 128, 196);\n"
"")
        self.menuinicial.addWidget(self.page_3)
        self.widget_2.raise_()
        self.frame_5.raise_()
        self.label_19.raise_()
        self.frame_4.raise_()
        self.frame_6.raise_()
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.widget_8 = QWidget(self.page_2)
        self.widget_8.setObjectName(u"widget_8")
        self.widget_8.setGeometry(QRect(1, 0, 331, 501))
        self.widget_8.setStyleSheet(u"background-color: rgb(255,255,255);")
        self.label_29 = QLabel(self.widget_8)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setGeometry(QRect(10, 200, 291, 291))
        self.label_29.setStyleSheet(u"background: transparent;\n"
"image: url(:/recursos/Convierte el logo de.png);")
        self.label_29.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_30 = QLabel(self.widget_8)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setGeometry(QRect(-15, 30, 331, 281))
        self.label_30.setStyleSheet(u"image: url(:/recursos/Cartoon-style illust.png);")
        self.label_30.raise_()
        self.label_29.raise_()
        self.widget_6 = QWidget(self.page_2)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setGeometry(QRect(310, 0, 401, 521))
        self.widget_6.setStyleSheet(u"background-color: rgb(20, 128, 196);")
        self.widget_7 = QWidget(self.widget_6)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setGeometry(QRect(40, 15, 311, 471))
        self.widget_7.setStyleSheet(u"background-color: rgb(55,147,205);\n"
"border-radius:8px;")
        self.label_27 = QLabel(self.widget_7)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setGeometry(QRect(20, 115, 271, 71))
        self.label_27.setStyleSheet(u"color: rgb(255,255,255);\n"
"font: 12pt \"Segoe UI\";\n"
"font: 600 20pt \"Segoe UI\";")
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pushButton_36 = QPushButton(self.widget_7)
        self.pushButton_36.setObjectName(u"pushButton_36")
        self.pushButton_36.setGeometry(QRect(170, 420, 91, 41))
        self.pushButton_36.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(238, 115, 58);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.pushButton_37 = QPushButton(self.widget_7)
        self.pushButton_37.setObjectName(u"pushButton_37")
        self.pushButton_37.setGeometry(QRect(60, 420, 91, 41))
        self.pushButton_37.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(20, 100, 156);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.label_28 = QLabel(self.widget_7)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QRect(105, 10, 101, 101))
        self.label_28.setStyleSheet(u"image: url(:/recursos/logocirculo.png);")
        self.comboBox_4 = QComboBox(self.widget_7)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")
        self.comboBox_4.setGeometry(QRect(160, 310, 121, 41))
        self.comboBox_4.setStyleSheet(u"border-radius:0px;\n"
"background-color: rgb(255, 255, 255);")
        self.label_17 = QLabel(self.widget_7)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(40, 200, 111, 21))
        self.label_17.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 600 9pt \"Segoe UI\";\n"
"font: 600 9pt \"Segoe UI\";")
        self.label_31 = QLabel(self.widget_7)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setGeometry(QRect(40, 230, 151, 16))
        self.label_31.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 600 9pt \"Segoe UI\";\n"
"font: 600 9pt \"Segoe UI\";")
        self.label_32 = QLabel(self.widget_7)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setGeometry(QRect(40, 260, 221, 16))
        self.label_32.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 600 9pt \"Segoe UI\";\n"
"font: 600 9pt \"Segoe UI\";")
        self.label_33 = QLabel(self.widget_7)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setGeometry(QRect(40, 310, 111, 41))
        self.label_33.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 600 9pt \"Segoe UI\";")
        self.label_34 = QLabel(self.widget_7)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setGeometry(QRect(10, 317, 31, 25))
        self.label_34.setStyleSheet(u"background-color: transparent;\n"
"image: url(:/inicio/person_24dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png);")
        self.menuinicial.addWidget(self.page_2)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.widget_3 = QWidget(self.page_4)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(309, -1, 401, 521))
        self.widget_3.setStyleSheet(u"background-color: rgb(20, 128, 196);")
        self.widget_5 = QWidget(self.widget_3)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setGeometry(QRect(40, 16, 311, 471))
        self.widget_5.setStyleSheet(u"background-color: rgb(55,147,205);\n"
"border-radius:8px;")
        self.label_23 = QLabel(self.widget_5)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setGeometry(QRect(20, 115, 271, 71))
        self.label_23.setStyleSheet(u"color: rgb(255,255,255);\n"
"font: 12pt \"Segoe UI\";\n"
"font: 600 20pt \"Segoe UI\";")
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_3 = QLineEdit(self.widget_5)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(25, 210, 261, 31))
        self.lineEdit_3.setStyleSheet(u"border-radius:12px;\n"
"background-color: rgb(255,255,255);")
        self.lineEdit_4 = QLineEdit(self.widget_5)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(25, 260, 261, 31))
        self.lineEdit_4.setStyleSheet(u"border-radius:12px;\n"
"background-color: rgb(255,255,255);")
        self.lineEdit_5 = QLineEdit(self.widget_5)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setGeometry(QRect(25, 310, 261, 31))
        self.lineEdit_5.setStyleSheet(u"border-radius:12px;\n"
"background-color: rgb(255,255,255);")
        self.lineEdit_6 = QLineEdit(self.widget_5)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setGeometry(QRect(25, 360, 261, 31))
        self.lineEdit_6.setStyleSheet(u"border-radius:12px;\n"
"background-color: rgb(255,255,255);")
        self.pushButton_34 = QPushButton(self.widget_5)
        self.pushButton_34.setObjectName(u"pushButton_34")
        self.pushButton_34.setGeometry(QRect(170, 420, 91, 41))
        self.pushButton_34.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(238, 115, 58);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.pushButton_35 = QPushButton(self.widget_5)
        self.pushButton_35.setObjectName(u"pushButton_35")
        self.pushButton_35.setGeometry(QRect(60, 420, 91, 41))
        self.pushButton_35.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(20, 100, 156);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.label_26 = QLabel(self.widget_5)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(QRect(105, 10, 101, 101))
        self.label_26.setStyleSheet(u"image: url(:/recursos/logocirculo.png);")
        self.widget_4 = QWidget(self.page_4)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setGeometry(QRect(0, 0, 331, 501))
        self.widget_4.setStyleSheet(u"background-color: rgb(255,255,255);")
        self.label_25 = QLabel(self.widget_4)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(10, 200, 291, 291))
        self.label_25.setStyleSheet(u"background: transparent;\n"
"image: url(:/recursos/Convierte el logo de.png);")
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_24 = QLabel(self.widget_4)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(-15, 30, 331, 281))
        self.label_24.setStyleSheet(u"image: url(:/recursos/Cartoon-style illust.png);")
        self.label_24.raise_()
        self.label_25.raise_()
        self.menuinicial.addWidget(self.page_4)
        self.widget_4.raise_()
        self.widget_3.raise_()
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.frame_3 = QFrame(self.page_5)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(-10, 0, 741, 81))
        self.frame_3.setStyleSheet(u"background-color: rgb(238, 115, 58);")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(90, 10, 231, 51))
        self.label_3.setStyleSheet(u"color: rgb(255,255,255);\n"
"font: 18pt \"Segoe UI\";\n"
"font: 600 20pt \"Segoe UI\";")
        self.label_9 = QLabel(self.frame_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(20, 10, 61, 61))
        self.label_9.setStyleSheet(u"image: url(:/recursos/logocirculo.png);")
        self.label_18 = QLabel(self.frame_3)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(600, -10, 91, 111))
        self.label_18.setStyleSheet(u"image: url(:/recursos/mapa de Baja Califor.png);")
        self.widget = QWidget(self.page_5)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 190, 681, 271))
        self.widget.setStyleSheet(u"image: url(:/recursos/autobusmarco.png);")
        self.pushButton_61 = QPushButton(self.widget)
        self.pushButton_61.setObjectName(u"pushButton_61")
        self.pushButton_61.setGeometry(QRect(450, 190, 34, 34))
        self.pushButton_61.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_61.setCheckable(True)
        self.pushButton_26 = QPushButton(self.widget)
        self.pushButton_26.setObjectName(u"pushButton_26")
        self.pushButton_26.setGeometry(QRect(270, 190, 34, 34))
        self.pushButton_26.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_26.setCheckable(True)
        self.pushButton_28 = QPushButton(self.widget)
        self.pushButton_28.setObjectName(u"pushButton_28")
        self.pushButton_28.setGeometry(QRect(450, 150, 34, 34))
        self.pushButton_28.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_28.setCheckable(True)
        self.pushButton_30 = QPushButton(self.widget)
        self.pushButton_30.setObjectName(u"pushButton_30")
        self.pushButton_30.setGeometry(QRect(390, 150, 34, 34))
        self.pushButton_30.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_30.setCheckable(True)
        self.pushButton_23 = QPushButton(self.widget)
        self.pushButton_23.setObjectName(u"pushButton_23")
        self.pushButton_23.setGeometry(QRect(270, 150, 34, 34))
        self.pushButton_23.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_23.setCheckable(True)
        self.pushButton_16 = QPushButton(self.widget)
        self.pushButton_16.setObjectName(u"pushButton_16")
        self.pushButton_16.setGeometry(QRect(570, 50, 34, 34))
        self.pushButton_16.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_16.setCheckable(True)
        self.pushButton_74 = QPushButton(self.widget)
        self.pushButton_74.setObjectName(u"pushButton_74")
        self.pushButton_74.setGeometry(QRect(130, 90, 34, 34))
        self.pushButton_74.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_74.setCheckable(True)
        self.pushButton_8 = QPushButton(self.widget)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(330, 50, 34, 34))
        self.pushButton_8.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_8.setCheckable(True)
        self.pushButton_63 = QPushButton(self.widget)
        self.pushButton_63.setObjectName(u"pushButton_63")
        self.pushButton_63.setGeometry(QRect(390, 190, 34, 34))
        self.pushButton_63.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_63.setCheckable(True)
        self.pushButton_70 = QPushButton(self.widget)
        self.pushButton_70.setObjectName(u"pushButton_70")
        self.pushButton_70.setGeometry(QRect(630, 150, 34, 34))
        self.pushButton_70.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_70.setCheckable(True)
        self.pushButton_66 = QPushButton(self.widget)
        self.pushButton_66.setObjectName(u"pushButton_66")
        self.pushButton_66.setGeometry(QRect(330, 190, 34, 34))
        self.pushButton_66.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_66.setCheckable(True)
        self.pushButton_65 = QPushButton(self.widget)
        self.pushButton_65.setObjectName(u"pushButton_65")
        self.pushButton_65.setGeometry(QRect(510, 150, 34, 34))
        self.pushButton_65.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_65.setCheckable(True)
        self.pushButton_11 = QPushButton(self.widget)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setGeometry(QRect(510, 50, 34, 34))
        self.pushButton_11.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_11.setCheckable(True)
        self.pushButton_69 = QPushButton(self.widget)
        self.pushButton_69.setObjectName(u"pushButton_69")
        self.pushButton_69.setGeometry(QRect(510, 190, 34, 34))
        self.pushButton_69.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_69.setCheckable(True)
        self.pushButton_17 = QPushButton(self.widget)
        self.pushButton_17.setObjectName(u"pushButton_17")
        self.pushButton_17.setGeometry(QRect(390, 50, 34, 34))
        self.pushButton_17.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_17.setCheckable(True)
        self.pushButton_13 = QPushButton(self.widget)
        self.pushButton_13.setObjectName(u"pushButton_13")
        self.pushButton_13.setGeometry(QRect(510, 90, 34, 34))
        self.pushButton_13.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_13.setCheckable(True)
        self.pushButton_73 = QPushButton(self.widget)
        self.pushButton_73.setObjectName(u"pushButton_73")
        self.pushButton_73.setGeometry(QRect(130, 150, 34, 34))
        self.pushButton_73.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_73.setCheckable(True)
        self.pushButton_15 = QPushButton(self.widget)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setGeometry(QRect(570, 90, 34, 34))
        self.pushButton_15.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_15.setCheckable(True)
        self.pushButton_6 = QPushButton(self.widget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(270, 50, 34, 34))
        self.pushButton_6.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_6.setCheckable(True)
        self.pushButton_14 = QPushButton(self.widget)
        self.pushButton_14.setObjectName(u"pushButton_14")
        self.pushButton_14.setGeometry(QRect(450, 90, 34, 34))
        self.pushButton_14.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_14.setCheckable(True)
        self.pushButton_9 = QPushButton(self.widget)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(330, 90, 34, 34))
        self.pushButton_9.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_9.setCheckable(True)
        self.pushButton_68 = QPushButton(self.widget)
        self.pushButton_68.setObjectName(u"pushButton_68")
        self.pushButton_68.setGeometry(QRect(570, 190, 34, 34))
        self.pushButton_68.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_68.setCheckable(True)
        self.pushButton_12 = QPushButton(self.widget)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setGeometry(QRect(450, 50, 34, 34))
        self.pushButton_12.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_12.setCheckable(True)
        self.pushButton_20 = QPushButton(self.widget)
        self.pushButton_20.setObjectName(u"pushButton_20")
        self.pushButton_20.setGeometry(QRect(630, 90, 34, 34))
        self.pushButton_20.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_20.setCheckable(True)
        self.pushButton_10 = QPushButton(self.widget)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setGeometry(QRect(270, 90, 34, 34))
        self.pushButton_10.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_10.setCheckable(True)
        self.pushButton_18 = QPushButton(self.widget)
        self.pushButton_18.setObjectName(u"pushButton_18")
        self.pushButton_18.setGeometry(QRect(390, 90, 34, 34))
        self.pushButton_18.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_18.setCheckable(True)
        self.pushButton_24 = QPushButton(self.widget)
        self.pushButton_24.setObjectName(u"pushButton_24")
        self.pushButton_24.setGeometry(QRect(570, 150, 34, 34))
        self.pushButton_24.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_24.setCheckable(True)
        self.pushButton_67 = QPushButton(self.widget)
        self.pushButton_67.setObjectName(u"pushButton_67")
        self.pushButton_67.setGeometry(QRect(330, 150, 34, 34))
        self.pushButton_67.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_67.setCheckable(True)
        self.pushButton_27 = QPushButton(self.widget)
        self.pushButton_27.setObjectName(u"pushButton_27")
        self.pushButton_27.setGeometry(QRect(630, 190, 34, 34))
        self.pushButton_27.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_27.setCheckable(True)
        self.pushButton_19 = QPushButton(self.widget)
        self.pushButton_19.setObjectName(u"pushButton_19")
        self.pushButton_19.setGeometry(QRect(630, 50, 34, 34))
        self.pushButton_19.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_19.setCheckable(True)
        self.pushButton_75 = QPushButton(self.widget)
        self.pushButton_75.setObjectName(u"pushButton_75")
        self.pushButton_75.setGeometry(QRect(210, 90, 34, 34))
        self.pushButton_75.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_75.setCheckable(True)
        self.pushButton_76 = QPushButton(self.widget)
        self.pushButton_76.setObjectName(u"pushButton_76")
        self.pushButton_76.setGeometry(QRect(210, 150, 34, 34))
        self.pushButton_76.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_76.setCheckable(True)
        self.pushButton_7 = QPushButton(self.widget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(130, 50, 34, 34))
        self.pushButton_7.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_7.setCheckable(True)
        self.pushButton_21 = QPushButton(self.widget)
        self.pushButton_21.setObjectName(u"pushButton_21")
        self.pushButton_21.setGeometry(QRect(210, 50, 34, 34))
        self.pushButton_21.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_21.setCheckable(True)
        self.pushButton_25 = QPushButton(self.widget)
        self.pushButton_25.setObjectName(u"pushButton_25")
        self.pushButton_25.setGeometry(QRect(210, 190, 34, 34))
        self.pushButton_25.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_25.setCheckable(True)
        self.pushButton_31 = QPushButton(self.widget)
        self.pushButton_31.setObjectName(u"pushButton_31")
        self.pushButton_31.setGeometry(QRect(130, 190, 34, 34))
        self.pushButton_31.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_31.setCheckable(True)
        self.pushButton_5 = QPushButton(self.page_5)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(600, 440, 81, 31))
        self.pushButton_5.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(238, 115, 58);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.pushButton_22 = QPushButton(self.page_5)
        self.pushButton_22.setObjectName(u"pushButton_22")
        self.pushButton_22.setGeometry(QRect(510, 440, 81, 31))
        self.pushButton_22.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(20, 100, 156);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.frame_2 = QFrame(self.page_5)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(10, 100, 681, 91))
        self.frame_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-radius:25px;")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.label_15 = QLabel(self.frame_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(510, 50, 21, 21))
        self.label_15.setStyleSheet(u"image: url(:/recursos/icon5.svg);")
        self.label_16 = QLabel(self.frame_2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(540, 50, 121, 20))
        self.label_16.setStyleSheet(u"color: rgb(229, 229, 229);\n"
"font: 16pt \"Segoe UI\";\n"
"font: 600 12pt \"Segoe UI\";")
        self.label_12 = QLabel(self.frame_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(400, 50, 101, 20))
        self.label_12.setStyleSheet(u"color: rgb(229, 229, 229);\n"
"font: 16pt \"Segoe UI\";\n"
"font: 600 12pt \"Segoe UI\";")
        self.label_13 = QLabel(self.frame_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(370, 50, 21, 21))
        self.label_13.setStyleSheet(u"image: url(:/recursos/icon3.svg);")
        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(260, 50, 21, 21))
        self.label_6.setStyleSheet(u"image: url(:/recursos/icon2.svg);")
        self.label_11 = QLabel(self.frame_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(290, 50, 71, 20))
        self.label_11.setStyleSheet(u"color: rgb(229, 229, 229);\n"
"font: 16pt \"Segoe UI\";\n"
"font: 600 12pt \"Segoe UI\";")
        self.label_10 = QLabel(self.frame_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(160, 50, 81, 20))
        self.label_10.setStyleSheet(u"color: rgb(229, 229, 229);\n"
"font: 16pt \"Segoe UI\";\n"
"font: 600 12pt \"Segoe UI\";")
        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(130, 50, 21, 21))
        self.label_4.setStyleSheet(u"image: url(:/recursos/icon.svg);")
        self.label_8 = QLabel(self.frame_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(50, 50, 71, 20))
        self.label_8.setStyleSheet(u"color: rgb(229, 229, 229);\n"
"font: 16pt \"Segoe UI\";\n"
"font: 600 12pt \"Segoe UI\";")
        self.label_14 = QLabel(self.frame_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(20, 50, 21, 21))
        self.label_14.setStyleSheet(u"image: url(:/recursos/icon4.svg);")
        self.label_7 = QLabel(self.frame_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(20, 10, 191, 31))
        self.label_7.setStyleSheet(u"font: 14pt \"Segoe UI\";")
        self.widget_12 = QWidget(self.page_5)
        self.widget_12.setObjectName(u"widget_12")
        self.widget_12.setGeometry(QRect(20, 230, 661, 191))
        self.widget_12.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.widget_13 = QWidget(self.page_5)
        self.widget_13.setObjectName(u"widget_13")
        self.widget_13.setGeometry(QRect(-11, -20, 741, 541))
        self.widget_13.setStyleSheet(u"background-color: rgb(20, 128, 196);")
        self.menuinicial.addWidget(self.page_5)
        self.widget_13.raise_()
        self.widget_12.raise_()
        self.frame_3.raise_()
        self.widget.raise_()
        self.pushButton_5.raise_()
        self.pushButton_22.raise_()
        self.frame_2.raise_()
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.widget_9 = QWidget(self.page_6)
        self.widget_9.setObjectName(u"widget_9")
        self.widget_9.setGeometry(QRect(1, 0, 331, 501))
        self.widget_9.setStyleSheet(u"background-color: rgb(255,255,255);")
        self.label_35 = QLabel(self.widget_9)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setGeometry(QRect(10, 200, 291, 291))
        self.label_35.setStyleSheet(u"image: url(:/recursos/Convierte el logo de.png);\n"
"background: transparent;")
        self.label_35.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_36 = QLabel(self.widget_9)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setGeometry(QRect(-15, 30, 331, 281))
        self.label_36.setStyleSheet(u"image: url(:/recursos/Cartoon-style illust.png);")
        self.label_36.raise_()
        self.label_35.raise_()
        self.widget_10 = QWidget(self.page_6)
        self.widget_10.setObjectName(u"widget_10")
        self.widget_10.setGeometry(QRect(310, 0, 401, 521))
        self.widget_10.setStyleSheet(u"background-color: rgb(20, 128, 196);")
        self.widget_11 = QWidget(self.widget_10)
        self.widget_11.setObjectName(u"widget_11")
        self.widget_11.setGeometry(QRect(40, 15, 311, 471))
        self.widget_11.setStyleSheet(u"background-color: rgb(55,147,205);\n"
"border-radius:8px;")
        self.label_37 = QLabel(self.widget_11)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setGeometry(QRect(20, 110, 271, 71))
        self.label_37.setStyleSheet(u"color: rgb(255,255,255);\n"
"font: 12pt \"Segoe UI\";\n"
"font: 600 20pt \"Segoe UI\";")
        self.label_37.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pushButton_38 = QPushButton(self.widget_11)
        self.pushButton_38.setObjectName(u"pushButton_38")
        self.pushButton_38.setGeometry(QRect(170, 420, 91, 41))
        self.pushButton_38.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(238, 115, 58);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.pushButton_39 = QPushButton(self.widget_11)
        self.pushButton_39.setObjectName(u"pushButton_39")
        self.pushButton_39.setGeometry(QRect(60, 420, 91, 41))
        self.pushButton_39.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(20, 100, 156);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.label_38 = QLabel(self.widget_11)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setGeometry(QRect(105, 10, 101, 101))
        self.label_38.setStyleSheet(u"border-image: url(:/recursos/logocirculo.png);")
        self.formapago = QStackedWidget(self.widget_11)
        self.formapago.setObjectName(u"formapago")
        self.formapago.setGeometry(QRect(19, 189, 271, 221))
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.comboBox_5 = QComboBox(self.page_7)
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.setObjectName(u"comboBox_5")
        self.comboBox_5.setGeometry(QRect(8, 10, 261, 31))
        self.comboBox_5.setStyleSheet(u"border-radius:0px;\n"
"background-color: rgb(255, 255, 255);")
        self.formapago.addWidget(self.page_7)
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.label_39 = QLabel(self.page_8)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setGeometry(QRect(20, 40, 49, 16))
        self.label_40 = QLabel(self.page_8)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setGeometry(QRect(20, 70, 49, 16))
        self.label_41 = QLabel(self.page_8)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setGeometry(QRect(20, 100, 49, 16))
        self.label_42 = QLabel(self.page_8)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setGeometry(QRect(20, 130, 49, 16))
        self.label_43 = QLabel(self.page_8)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setGeometry(QRect(130, 40, 49, 16))
        self.label_44 = QLabel(self.page_8)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setGeometry(QRect(130, 70, 49, 16))
        self.label_45 = QLabel(self.page_8)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setGeometry(QRect(20, 170, 49, 16))
        self.label_46 = QLabel(self.page_8)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setGeometry(QRect(20, 200, 81, 16))
        self.label_47 = QLabel(self.page_8)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setGeometry(QRect(130, 100, 81, 16))
        self.label_48 = QLabel(self.page_8)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setGeometry(QRect(18, 10, 111, 20))
        self.lineEdit = QLineEdit(self.page_8)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(110, 196, 113, 21))
        self.lineEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.formapago.addWidget(self.page_8)
        self.page_10 = QWidget()
        self.page_10.setObjectName(u"page_10")
        self.label_49 = QLabel(self.page_10)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setGeometry(QRect(20, 20, 131, 41))
        self.formapago.addWidget(self.page_10)
        self.formapago.raise_()
        self.label_37.raise_()
        self.pushButton_38.raise_()
        self.pushButton_39.raise_()
        self.label_38.raise_()
        self.menuinicial.addWidget(self.page_6)
        self.page_9 = QWidget()
        self.page_9.setObjectName(u"page_9")
        self.menuinicial.addWidget(self.page_9)
        loginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(loginWindow)

        self.menuinicial.setCurrentIndex(1)
        self.formapago.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(loginWindow)
    # setupUi

    def retranslateUi(self, loginWindow):
        loginWindow.setWindowTitle(QCoreApplication.translate("loginWindow", u"MainWindow", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("loginWindow", u"Rutas Baja Express", None))
        self.label_5.setText("")
#if QT_CONFIG(whatsthis)
        self.pushButton.setWhatsThis(QCoreApplication.translate("loginWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.pushButton.setText(QCoreApplication.translate("loginWindow", u"Terminales disponibles", None))
#if QT_CONFIG(whatsthis)
        self.pushButton_2.setWhatsThis(QCoreApplication.translate("loginWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.pushButton_2.setText(QCoreApplication.translate("loginWindow", u"Vender boletos", None))
#if QT_CONFIG(whatsthis)
        self.pushButton_3.setWhatsThis(QCoreApplication.translate("loginWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.pushButton_3.setText(QCoreApplication.translate("loginWindow", u"Configuracion", None))
#if QT_CONFIG(whatsthis)
        self.pushButton_4.setWhatsThis(QCoreApplication.translate("loginWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.pushButton_4.setText(QCoreApplication.translate("loginWindow", u"Cerrar sesion", None))
#if QT_CONFIG(whatsthis)
        self.pushButton_40.setWhatsThis(QCoreApplication.translate("loginWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.pushButton_40.setText(QCoreApplication.translate("loginWindow", u"Viajes", None))
        self.pushButton_33.setText(QCoreApplication.translate("loginWindow", u"Regresar", None))
        self.label_50.setText("")
        self.label_51.setText(QCoreApplication.translate("loginWindow", u"11:00AM", None))
        self.label_52.setText(QCoreApplication.translate("loginWindow", u"23 Nov", None))
        self.label_53.setText("")
        self.label_54.setText(QCoreApplication.translate("loginWindow", u"10 horas 30 min", None))
        self.label_55.setText(QCoreApplication.translate("loginWindow", u"11:00AM", None))
        self.pushButton_41.setText("")
        self.label_56.setText(QCoreApplication.translate("loginWindow", u"23 Nov", None))
        self.label_57.setText("")
        self.label_58.setText("")
        self.label_59.setText(QCoreApplication.translate("loginWindow", u"$1500 MXN", None))
        self.label_60.setText(QCoreApplication.translate("loginWindow", u"Tijuana", None))
        self.label_61.setText(QCoreApplication.translate("loginWindow", u"San Quintin", None))
        self.label_19.setText(QCoreApplication.translate("loginWindow", u"Viajes disponibles:", None))
        self.pushButton_29.setText("")
        self.comboBox.setItemText(0, QCoreApplication.translate("loginWindow", u"Tijuana B.C", None))

        self.comboBox.setPlaceholderText(QCoreApplication.translate("loginWindow", u"Origen", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("loginWindow", u"Mexicali B.C.", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("loginWindow", u"Ensenada B.C", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("loginWindow", u"Tecate B.C.", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("loginWindow", u"Rosarito B.C.", None))
        self.comboBox_2.setItemText(4, QCoreApplication.translate("loginWindow", u"San Quint\u00edn B.C.", None))
        self.comboBox_2.setItemText(5, QCoreApplication.translate("loginWindow", u"San Felipe B.C.", None))

        self.comboBox_2.setPlaceholderText(QCoreApplication.translate("loginWindow", u"Destino", None))
        self.fecha.setSpecialValueText(QCoreApplication.translate("loginWindow", u"\" \"", None))
        self.fecha.setDisplayFormat(QCoreApplication.translate("loginWindow", u"M", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("loginWindow", u"1", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("loginWindow", u"2", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("loginWindow", u"3", None))
        self.comboBox_3.setItemText(3, QCoreApplication.translate("loginWindow", u"4", None))
        self.comboBox_3.setItemText(4, QCoreApplication.translate("loginWindow", u"5", None))
        self.comboBox_3.setItemText(5, QCoreApplication.translate("loginWindow", u"6", None))
        self.comboBox_3.setItemText(6, QCoreApplication.translate("loginWindow", u"7", None))
        self.comboBox_3.setItemText(7, QCoreApplication.translate("loginWindow", u"8", None))
        self.comboBox_3.setItemText(8, QCoreApplication.translate("loginWindow", u"9", None))
        self.comboBox_3.setItemText(9, QCoreApplication.translate("loginWindow", u"10", None))

        self.comboBox_3.setPlaceholderText(QCoreApplication.translate("loginWindow", u"Pasajeros", None))
        self.label_20.setText(QCoreApplication.translate("loginWindow", u"Rutas Baja Express", None))
        self.label_21.setText("")
        self.label_22.setText("")
#if QT_CONFIG(whatsthis)
        self.label_29.setWhatsThis(QCoreApplication.translate("loginWindow", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.label_29.setText("")
        self.label_30.setText("")
        self.label_27.setText(QCoreApplication.translate("loginWindow", u"Tipo de\n"
" pasajero", None))
        self.pushButton_36.setText(QCoreApplication.translate("loginWindow", u"Cancelar", None))
        self.pushButton_37.setText(QCoreApplication.translate("loginWindow", u"Siguiente", None))
        self.label_28.setText("")
        self.comboBox_4.setItemText(0, QCoreApplication.translate("loginWindow", u"Adulto", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("loginWindow", u"Ni\u00f1o", None))
        self.comboBox_4.setItemText(2, QCoreApplication.translate("loginWindow", u"INAPAM", None))

        self.label_17.setText(QCoreApplication.translate("loginWindow", u"Lista de descuentos:", None))
        self.label_31.setText(QCoreApplication.translate("loginWindow", u"Ni\u00f1os (Menores a 10 a\u00f1os)", None))
        self.label_32.setText(QCoreApplication.translate("loginWindow", u"Adultos Mayores (Apartir de los 60 a\u00f1os)", None))
        self.label_33.setText(QCoreApplication.translate("loginWindow", u"Pasajero #", None))
        self.label_34.setText("")
        self.label_23.setText(QCoreApplication.translate("loginWindow", u"Registro de\n"
"pasajeros", None))
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("loginWindow", u"  Nombre", None))
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("loginWindow", u"  Primer Apellido", None))
        self.lineEdit_5.setPlaceholderText(QCoreApplication.translate("loginWindow", u"  Segundo Apellido", None))
        self.lineEdit_6.setPlaceholderText(QCoreApplication.translate("loginWindow", u"  Fecha de nacimiento (dd/mm/aaa)", None))
        self.pushButton_34.setText(QCoreApplication.translate("loginWindow", u"Cancelar", None))
        self.pushButton_35.setText(QCoreApplication.translate("loginWindow", u"Siguiente", None))
        self.label_26.setText("")
#if QT_CONFIG(whatsthis)
        self.label_25.setWhatsThis(QCoreApplication.translate("loginWindow", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.label_25.setText("")
        self.label_24.setText("")
        self.label_3.setText(QCoreApplication.translate("loginWindow", u"Rutas Baja Express", None))
        self.label_9.setText("")
        self.label_18.setText("")
        self.pushButton_61.setText(QCoreApplication.translate("loginWindow", u"29", None))
        self.pushButton_26.setText(QCoreApplication.translate("loginWindow", u"23", None))
        self.pushButton_28.setText(QCoreApplication.translate("loginWindow", u"30", None))
        self.pushButton_30.setText(QCoreApplication.translate("loginWindow", u"28", None))
        self.pushButton_23.setText(QCoreApplication.translate("loginWindow", u"24", None))
        self.pushButton_16.setText(QCoreApplication.translate("loginWindow", u"16", None))
        self.pushButton_74.setText(QCoreApplication.translate("loginWindow", u"       1", None))
        self.pushButton_8.setText(QCoreApplication.translate("loginWindow", u"8", None))
        self.pushButton_63.setText(QCoreApplication.translate("loginWindow", u"27", None))
        self.pushButton_70.setText(QCoreApplication.translate("loginWindow", u"36", None))
        self.pushButton_66.setText(QCoreApplication.translate("loginWindow", u"25", None))
        self.pushButton_65.setText(QCoreApplication.translate("loginWindow", u"32", None))
        self.pushButton_11.setText(QCoreApplication.translate("loginWindow", u"14", None))
        self.pushButton_69.setText(QCoreApplication.translate("loginWindow", u"31", None))
        self.pushButton_17.setText(QCoreApplication.translate("loginWindow", u"10", None))
        self.pushButton_13.setText(QCoreApplication.translate("loginWindow", u"13", None))
        self.pushButton_73.setText(QCoreApplication.translate("loginWindow", u"      20", None))
        self.pushButton_15.setText(QCoreApplication.translate("loginWindow", u"15", None))
        self.pushButton_6.setText(QCoreApplication.translate("loginWindow", u"6", None))
        self.pushButton_14.setText(QCoreApplication.translate("loginWindow", u"11", None))
        self.pushButton_9.setText(QCoreApplication.translate("loginWindow", u"7", None))
        self.pushButton_68.setText(QCoreApplication.translate("loginWindow", u"33", None))
        self.pushButton_12.setText(QCoreApplication.translate("loginWindow", u"12", None))
        self.pushButton_20.setText(QCoreApplication.translate("loginWindow", u"17", None))
        self.pushButton_10.setText(QCoreApplication.translate("loginWindow", u"5", None))
        self.pushButton_18.setText(QCoreApplication.translate("loginWindow", u"9", None))
        self.pushButton_24.setText(QCoreApplication.translate("loginWindow", u"34", None))
        self.pushButton_67.setText(QCoreApplication.translate("loginWindow", u"26", None))
        self.pushButton_27.setText(QCoreApplication.translate("loginWindow", u"35", None))
        self.pushButton_19.setText(QCoreApplication.translate("loginWindow", u"18", None))
        self.pushButton_75.setText(QCoreApplication.translate("loginWindow", u"3", None))
        self.pushButton_76.setText(QCoreApplication.translate("loginWindow", u"22", None))
        self.pushButton_7.setText(QCoreApplication.translate("loginWindow", u"2", None))
        self.pushButton_21.setText(QCoreApplication.translate("loginWindow", u"4", None))
        self.pushButton_25.setText(QCoreApplication.translate("loginWindow", u"21", None))
        self.pushButton_31.setText(QCoreApplication.translate("loginWindow", u"19", None))
        self.pushButton_5.setText(QCoreApplication.translate("loginWindow", u"Regresar", None))
        self.pushButton_22.setText(QCoreApplication.translate("loginWindow", u"Aceptar", None))
        self.label_15.setText("")
        self.label_16.setText(QCoreApplication.translate("loginWindow", u"Asiento especial", None))
        self.label_12.setText(QCoreApplication.translate("loginWindow", u"Seleccionado", None))
        self.label_13.setText("")
        self.label_6.setText("")
        self.label_11.setText(QCoreApplication.translate("loginWindow", u"Seleccion", None))
        self.label_10.setText(QCoreApplication.translate("loginWindow", u"Disponible", None))
        self.label_4.setText("")
        self.label_8.setText(QCoreApplication.translate("loginWindow", u"Ocupado", None))
        self.label_14.setText("")
        self.label_7.setText(QCoreApplication.translate("loginWindow", u"Selecci\u00f3n de asientos", None))
#if QT_CONFIG(whatsthis)
        self.label_35.setWhatsThis(QCoreApplication.translate("loginWindow", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.label_35.setText("")
        self.label_36.setText("")
        self.label_37.setText(QCoreApplication.translate("loginWindow", u"Forma de pago", None))
        self.pushButton_38.setText(QCoreApplication.translate("loginWindow", u"Cancelar", None))
        self.pushButton_39.setText(QCoreApplication.translate("loginWindow", u"Siguiente", None))
        self.label_38.setText("")
        self.comboBox_5.setItemText(0, QCoreApplication.translate("loginWindow", u"Efectivo", None))
        self.comboBox_5.setItemText(1, QCoreApplication.translate("loginWindow", u"Tarjeta", None))

        self.label_39.setText(QCoreApplication.translate("loginWindow", u"Persona", None))
        self.label_40.setText(QCoreApplication.translate("loginWindow", u"Camion", None))
        self.label_41.setText(QCoreApplication.translate("loginWindow", u"Asiento", None))
        self.label_42.setText(QCoreApplication.translate("loginWindow", u"Precio", None))
        self.label_43.setText(QCoreApplication.translate("loginWindow", u"Origen", None))
        self.label_44.setText(QCoreApplication.translate("loginWindow", u"Destino", None))
        self.label_45.setText(QCoreApplication.translate("loginWindow", u"Total:", None))
        self.label_46.setText(QCoreApplication.translate("loginWindow", u"Total recibido:", None))
        self.label_47.setText(QCoreApplication.translate("loginWindow", u"Tipo de pago", None))
        self.label_48.setText(QCoreApplication.translate("loginWindow", u"Resumen de compra", None))
        self.label_49.setText(QCoreApplication.translate("loginWindow", u"Pedir datos de tarjeta", None))
    # retranslateUi

