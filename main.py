import sys
import os
from PyQt5.QtWidgets import QApplication
from ventanas.ventanaPrincipal import VentanaPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Lanza la ventana principal
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())