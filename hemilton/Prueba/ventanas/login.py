# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QStackedWidget, QWidget)
from ventanas import recursos_rc

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
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(70, 10, 131, 121))
        self.label_5.setStyleSheet(u"image: url(:/recursos/logocirculo.png);")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(60, 180, 151, 51))
        self.label_7.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 16pt \"Segoe UI\";\n"
"font: 600 16pt \"Segoe UI\";")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 130, 231, 51))
        self.label_2.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 18pt \"Segoe UI\";\n"
"font: 600 20pt \"Segoe UI\";")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(270, -10, 441, 511))
        self.label.setStyleSheet(u"image: url(:/recursos/auto1.jpg);")
        self.login = QStackedWidget(self.centralwidget)
        self.login.setObjectName(u"login")
        self.login.setGeometry(QRect(10, 230, 251, 261))
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.lineEdit_4 = QLineEdit(self.page_5)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(20, 30, 211, 41))
        self.lineEdit_5 = QLineEdit(self.page_5)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setGeometry(QRect(20, 80, 211, 41))
        self.pushButton_5 = QPushButton(self.page_5)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(40, 130, 171, 41))
        self.pushButton_5.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(20, 128, 196);\n"
"font: 600 14pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.label_8 = QLabel(self.page_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 200, 121, 51))
        self.label_8.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 9pt \"Segoe UI\";")
        self.pushButton_6 = QPushButton(self.page_5)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(140, 210, 111, 31))
        self.pushButton_6.setStyleSheet(u"background-color: rgb(238, 115, 58);\n"
"font: 600 9pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.login.addWidget(self.page_5)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.widget_2 = QWidget(self.page_6)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(20, 30, 221, 91))
        self.widget_2.setStyleSheet(u"image: url(:/inicio/warning.png);")
        self.pushButton_7 = QPushButton(self.page_6)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(40, 130, 171, 41))
        self.pushButton_7.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(238, 115, 58);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.pushButton_8 = QPushButton(self.page_6)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(40, 180, 171, 41))
        self.pushButton_8.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(21, 128, 196);\n"
"font: 600 12pt \"Segoe UI\";\n"
"border-radius:12px;")
        self.login.addWidget(self.page_6)
        loginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(loginWindow)

        self.login.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(loginWindow)
    # setupUi

    def retranslateUi(self, loginWindow):
        loginWindow.setWindowTitle(QCoreApplication.translate("loginWindow", u"MainWindow", None))
        self.label_5.setText("")
        self.label_7.setText(QCoreApplication.translate("loginWindow", u"Inicio de sesi\u00f3n", None))
        self.label_2.setText(QCoreApplication.translate("loginWindow", u"Rutas Baja Express", None))
        self.label.setText("")
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("loginWindow", u"Usuario", None))
        self.lineEdit_5.setPlaceholderText(QCoreApplication.translate("loginWindow", u"Contrase\u00f1a", None))
        self.pushButton_5.setText(QCoreApplication.translate("loginWindow", u"Acceder", None))
#if QT_CONFIG(tooltip)
        self.label_8.setToolTip(QCoreApplication.translate("loginWindow", u"<html><head/><body><p align=\"right\"><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_8.setText(QCoreApplication.translate("loginWindow", u"Aun no tienes cuenta?", None))
        self.pushButton_6.setText(QCoreApplication.translate("loginWindow", u"Registrate aqu\u00ed", None))
        self.pushButton_7.setText(QCoreApplication.translate("loginWindow", u"Intentar de nuevo", None))
        self.pushButton_8.setText(QCoreApplication.translate("loginWindow", u"Salir", None))
    # retranslateUi

