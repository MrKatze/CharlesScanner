from PyQt5.QtWidgets import *
from ventanas.VentanaRuta import VentanaSeleccionarRuta
import qtawesome as qta
from PyQt5.QtCore import QSize, Qt
class VentanaConfiguracion(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Opciones")
        self.setGeometry(300, 200, 300, 200)
        
        # Aplicar estilos generales a la ventana
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #cfcfcf;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3);
            }
            QToolButton {
                background-color: white;
                color: black;
                border-radius: 5px;
                padding: 5px 10px;
                border: 1px solid #cfcfcf;
            }
            QToolButton:hover {
                background-color: #0056b3;
            }
            QToolButton:disabled {
                background-color: #e6e6e6;
                color: #a0a0a0;
            }
            QLabel {
                font-family: Arial, sans-serif;
                font-size: 12pt;
            }
        """)
        layout = QHBoxLayout()
        
        
        self.btnCamara = QToolButton()
        self.btnCamara.setText("Abrir Cámara")
      #  self.btnCamara.setFixedSize(90, 120)  # Anchura = 100 px, Altura = 80 px
        self.btnCamara.setIcon(qta.icon("fa5s.camera"))  # Ícono de FontAwesome
        self.btnCamara.setIconSize(QSize(40, 40))  # Ajusta el tamaño del icono
        self.btnCamara.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # Texto debajo del icono
        self.btnCamara.clicked.connect(self.realizar_opcion)
        layout.addWidget(self.btnCamara)

        self.btnRuta = QToolButton()
        self.btnRuta.setText("Cambiar Ruta")
       # self.btnRuta.setFixedSize(90, 120)  # Anchura = 100 px, Altura = 80 px
        self.btnRuta.setIcon(qta.icon("fa5s.folder"))  
        self.btnRuta.setIconSize(QSize(40, 40))
        self.btnRuta.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btnRuta.clicked.connect(self.realizar_opcion)
        layout.addWidget(self.btnRuta)
        
        self.setLayout(layout)

    def realizar_opcion(self):
        boton_presionado = self.sender()

        if boton_presionado.text() == "Abrir Cámara":
          #  print("Cámara activada")  # Aquí podrías añadir la integración con OpenCV
            
            self.close()
        elif boton_presionado.text() == "Cambiar Ruta":
            self.close()
            tarjeta = VentanaSeleccionarRuta()
            tarjeta.exec_()
           # print("Opción alternativa seleccionada")  # Acción para la otra opción