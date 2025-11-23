from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QToolButton
from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt, QDate
import sys

# Login
from ventanas.login import Ui_loginWindow

# Menu inicial
from ventanas.menuinicial import Ui_loginWindow as Ui_MenuInicial


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Cargar pantalla de login ---
        self.login_ui = Ui_loginWindow()
        self.login_ui.setupUi(self)

        # --- Agregar iconos tipo placeholder al login ---
        self.agregar_iconos_placeholder_login()

        # Conectar botón ACCEDER
        self.login_ui.pushButton_5.clicked.connect(self.validar_login)

        # Conectar botones de la página 6 (error)
        self.login_ui.pushButton_7.clicked.connect(self.reintentar_login)
        self.login_ui.pushButton_8.clicked.connect(self.salir)

    # ====================================
    #   AGREGAR ICONOS COMO PLACEHOLDER EN LOGIN
    # ====================================
    def agregar_iconos_placeholder_login(self):
        icono_person = QIcon(":/recursos/person.png")
        accion_person = self.login_ui.lineEdit_4.addAction(icono_person, QLineEdit.LeadingPosition)
        accion_person.setVisible(True)

        icono_lock = QIcon(":/recursos/lock.png")
        accion_lock = self.login_ui.lineEdit_5.addAction(icono_lock, QLineEdit.LeadingPosition)
        accion_lock.setVisible(True)

        self.login_ui.lineEdit_4.textChanged.connect(lambda text: accion_person.setVisible(not bool(text)))
        self.login_ui.lineEdit_5.textChanged.connect(lambda text: accion_lock.setVisible(not bool(text)))

    # ====================================
    #    VALIDAR USUARIO / CONTRASEÑA
    # ====================================
    def validar_login(self):
        usuario = self.login_ui.lineEdit_4.text()
        password = self.login_ui.lineEdit_5.text()
        if usuario == "admin" and password == "1234":
            self.mostrar_menu()
        else:
            self.login_ui.login.setCurrentIndex(1)

    # ====================================
    #   REINTENTAR LOGIN
    # ====================================
    def reintentar_login(self):
        self.login_ui.lineEdit_4.clear()
        self.login_ui.lineEdit_5.clear()
        self.login_ui.login.setCurrentIndex(0)

    # ====================================
    #   CERRAR APP
    # ====================================
    def salir(self):
        sys.exit(0)

    # ====================================
    #   MOSTRAR MENÚ INICIAL
    # ====================================
    def mostrar_menu(self):
        self.menu_ui = Ui_MenuInicial()
        self.menu_ui.setupUi(self)

        # Conexiones de botones
        self.menu_ui.pushButton_2.clicked.connect(lambda: self.menu_ui.menuinicial.setCurrentIndex(1))
        self.menu_ui.pushButton_33.clicked.connect(lambda: self.menu_ui.menuinicial.setCurrentIndex(0))
        self.menu_ui.pushButton_29.clicked.connect(lambda: self.menu_ui.menuinicial.setCurrentIndex(2))
        self.menu_ui.pushButton_36.clicked.connect(lambda: self.menu_ui.menuinicial.setCurrentIndex(1))
        self.menu_ui.pushButton_41.clicked.connect(lambda: self.menu_ui.menuinicial.setCurrentIndex(2))
        self.menu_ui.pushButton_34.clicked.connect(lambda: self.menu_ui.menuinicial.setCurrentIndex(2))
        self.menu_ui.pushButton_27.clicked.connect(lambda: self.menu_ui.menuinicial.setCurrentIndex(3))
        self.menu_ui.pushButton_5.clicked.connect(lambda: self.menu_ui.menuinicial.setCurrentIndex(3))
        self.menu_ui.pushButton_37.clicked.connect(lambda: self.menu_ui.menuinicial.setCurrentIndex(3))
        self.menu_ui.pushButton_35.clicked.connect(lambda: self.menu_ui.menuinicial.setCurrentIndex(4))
        self.menu_ui.pushButton_22.clicked.connect(lambda: self.menu_ui.menuinicial.setCurrentIndex(5))
        self.menu_ui.pushButton_38.clicked.connect(lambda: self.menu_ui.menuinicial.setCurrentIndex(4))

        self.menu_ui.comboBox_5.currentIndexChanged.connect(self.cambiar_pago)

        # -------------------------
        #  Placeholders visuales para ComboBox page_3 con icono NO seleccionable
        # -------------------------
        def agregar_placeholder(combo, texto, icono):
            model = QStandardItemModel()
            placeholder_item = QStandardItem(icono, texto)
            placeholder_item.setEnabled(False)
            model.appendRow(placeholder_item)

            for i in range(combo.count()):
                item = QStandardItem(combo.itemText(i))
                model.appendRow(item)

            combo.setModel(model)
            combo.setCurrentIndex(0)

        icon_location = QIcon(":/recursos/location.svg")
        icon_groups = QIcon(":/recursos/groups.svg")

        agregar_placeholder(self.menu_ui.comboBox, "Origen", icon_location)
        agregar_placeholder(self.menu_ui.comboBox_2, "Destino", icon_location)
        agregar_placeholder(self.menu_ui.comboBox_3, "Pasajeros", icon_groups)

        # -------------------------
        #  QDATEEDIT con placeholder "Fecha" y calendario en fecha actual
        # -------------------------
        self.menu_ui.fecha.setCalendarPopup(True)
        self.menu_ui.fecha.setDisplayFormat("dd/MM/yyyy")

        # Colocar la fecha actual como mínima para poder usar specialValueText
        hoy = QDate.currentDate()
        self.menu_ui.fecha.setMinimumDate(hoy)
        self.menu_ui.fecha.setDate(hoy)
        self.menu_ui.fecha.setSpecialValueText("Fecha")

        # Evitar que escriban
        self.menu_ui.fecha.lineEdit().setReadOnly(True)
        self.menu_ui.fecha.setKeyboardTracking(False)

        # Icono como botón interno
        icono = QIcon(":/recursos/calendar.svg")
        self.btn_fecha = QToolButton(self.menu_ui.fecha)
        self.btn_fecha.setIcon(icono)
        self.btn_fecha.setCursor(Qt.PointingHandCursor)
        self.btn_fecha.setStyleSheet("border: none; padding: 0px;")
        self.btn_fecha.setFixedSize(20, 20)
        self.menu_ui.fecha.showEvent = self.posicionar_icono_fecha
        self.menu_ui.fecha.setStyleSheet("""
            QDateEdit {
                padding-left: 22px;
            }
        """)

    # Reubicar icono cuando el widget ya existe
    def posicionar_icono_fecha(self, event):
        self.btn_fecha.move(6, (self.menu_ui.fecha.height() - self.btn_fecha.height()) // 2)

    # ====================================
    #   CAMBIAR ENTRE MÉTODOS DE PAGO
    # ====================================
    def cambiar_pago(self):
        metodo = self.menu_ui.comboBox_5.currentText()
        if metodo.lower() == "efectivo":
            self.menu_ui.formapago.setCurrentIndex(1)
        else:
            self.menu_ui.formapago.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())