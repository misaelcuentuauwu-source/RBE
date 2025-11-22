from PySide6.QtWidgets import QApplication, QMainWindow
import sys

# Login
from ventanas.login import Ui_loginWindow

# Menu inicial
from ventanas.menuinicial import Ui_loginWindow as Ui_MenuInicial


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar login primero
        self.login_ui = Ui_loginWindow()
        self.login_ui.setupUi(self)

        # Cambia "pushButton_5" por el botón correcto para ACCEDER
        self.login_ui.pushButton_5.clicked.connect(self.mostrar_menu)

    # -------------------------
    #   CAMBIAR A MENU INICIAL
    # -------------------------
    def mostrar_menu(self):
        self.menu_ui = Ui_MenuInicial()
        self.menu_ui.setupUi(self)

        # ================
        # NAVEGACIÓN PEDIDA
        # ================

        # 1) Comprar boletos → page_3
        self.menu_ui.pushButton_comprar.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(1)
        )

        # 2) En page_3 → pushButton_29 → page_2
        self.menu_ui.pushButton_29.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(2)
        )

        # 3) En page_2 → boton siguiente → page_4
        self.menu_ui.pushButton_siguiente_p2.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(3)
        )

        # 4) En page_4 → boton siguiente → page_5
        self.menu_ui.pushButton_siguiente_p4.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(4)
        )

        # 5) En page_5 → aceptar → page_6
        self.menu_ui.pushButton_aceptar_p5.clicked.connect(
            lambda: self.menu_ui.menuinicial.setCurrentIndex(5)
        )

        # -------------------------------
        #   STACKEDWIDGET INTERNO EN PAGE 6
        # -------------------------------
        # combo box: self.menu_ui.comboBox_pago
        # stacked interno: self.menu_ui.stacked_pago
        # página resumen: index 1 (por ejemplo)

        self.menu_ui.comboBox_pago.currentIndexChanged.connect(self.cambiar_pago)

    # -------------------------
    #  CAMBIA ENTRE PAGO/RESUMEN
    # -------------------------
    def cambiar_pago(self):
        metodo = self.menu_ui.comboBox_pago.currentText()

        if metodo.lower() == "efectivo":
            # mostrar página donde está “Resumen de compra”
            self.menu_ui.stacked_pago.setCurrentIndex(1)
        else:
            # mostrar página normal
            self.menu_ui.stacked_pago.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())