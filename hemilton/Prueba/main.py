from PySide6.QtWidgets import QApplication, QMainWindow
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

        # Conectar botón ACCEDER
        self.login_ui.pushButton_5.clicked.connect(self.validar_login)

        # Conectar botones de la página 6 (error)
        self.login_ui.pushButton_7.clicked.connect(self.reintentar_login)
        self.login_ui.pushButton_8.clicked.connect(self.salir)

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

        # -------------------------
        #  Aquí conectamos botones
        # -------------------------

        # VENDER BOLETOS → PAGE_3
        self.menu_ui.pushButton_2.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(1)
        )
        
        # pa que se regrese#
        self.menu_ui.pushButton_33.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(0)
        )

        # En page_3 → pushButton_29 → page_2
        self.menu_ui.pushButton_29.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(2)
        )
         # pa que se regrese#
        self.menu_ui.pushButton_36.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(1)
        )


        # ⭐ NUEVO: En page_3 → pushButton_41 → page_2
        self.menu_ui.pushButton_41.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(2)
        )
         # pa que se regrese#
        self.menu_ui.pushButton_34.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(2)
        )
        
        

        # ⭐ NUEVO: En page_2 → pushButton_27 → page_4
        self.menu_ui.pushButton_27.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(3)
        )
        # pa que se regrese#
        self.menu_ui.pushButton_5.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(3)
        )
        
        
        # En page_2 → siguiente → page_4 (botón previo tuyo)
        self.menu_ui.pushButton_37.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(3)
        )

        # En page_4 → siguiente → page_5
        self.menu_ui.pushButton_35.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(4)
        )

        # En page_5 → aceptar → page_6
        self.menu_ui.pushButton_22.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(5)
        )
        # Combo de pago en page_6
        self.menu_ui.comboBox_pago.currentIndexChanged.connect(self.cambiar_pago)

    # ====================================
    #   CAMBIAR ENTRE MÉTODOS DE PAGO
    # ====================================
    def cambiar_pago(self):
        metodo = self.menu_ui.comboBox_pago.currentText()

        if metodo.lower() == "efectivo":
            self.menu_ui.stacked_pago.setCurrentIndex(1)
        else:
            self.menu_ui.stacked_pago.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())