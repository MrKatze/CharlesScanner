from PyQt5.QtWidgets import *
from ventanas.VentanaRuta import VentanaSeleccionarRuta

class VentanaConfiguracion(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Opciones")
        self.setGeometry(300, 200, 300, 200)
        
        # Agregar un borde visible al diálogo
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout()
        
       # label = QLabel("Seleccione una acción:")
      #  layout.addWidget(label)
        
        btnEditar = QPushButton("Abrir Cámara")
        btnEditar.clicked.connect(self.realizar_opcion)
        layout.addWidget(btnEditar)
        
         # Otro botón para otra opción
        btn_otro = QPushButton("Otra opción")
        btn_otro.clicked.connect(self.realizar_opcion)  # Conectamos al mismo método
        layout.addWidget(btn_otro)
        
        self.setLayout(layout)

    def realizar_opcion(self):
        boton_presionado = self.sender()

        if boton_presionado.text() == "Abrir Cámara":
            print("Cámara activada")  # Aquí podrías añadir la integración con OpenCV
        elif boton_presionado.text() == "Otra opción":
            self.close()
            tarjeta = VentanaSeleccionarRuta()
            tarjeta.exec_()
            print("Opción alternativa seleccionada")  # Acción para la otra opción