from PyQt5.QtWidgets import *
from app.Extraer_texto import extraccion
from PyQt5.QtCore import Qt

class VentanaGuardadoArchivo(QDialog):
    def __init__(self, ImagenProcesada):
        super().__init__()
        self.setWindowTitle("Opciones")
        self.setGeometry(300, 200, 300, 200)
        self.imagenProcesada = ImagenProcesada

        # Agregar un borde visible al diálogo
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout()

        label = QLabel("Introduce el nombre del archivo:")
        layout.addWidget(label)

        # Campo de entrada para el nombre de archivo
        self.nombreArchivo = QLineEdit()
        layout.addWidget(self.nombreArchivo)

        # Botón para guardar en formato PDF
        self.btnPDF = QPushButton("Guardar en formato pdf")
        self.btnPDF.setEnabled(False)  # Desactivado inicialmente
        self.btnPDF.clicked.connect(self.realizar_opcion)
        layout.addWidget(self.btnPDF)

        # Botón para guardar en formato DOCX
        self.btnWORD = QPushButton("Guardar en formato docx")
        self.btnWORD.setEnabled(False)  # Desactivado inicialmente
        self.btnWORD.clicked.connect(self.realizar_opcion)
        layout.addWidget(self.btnWORD)

        # Conexión para habilitar botones cuando se ingrese texto
        self.nombreArchivo.textChanged.connect(self.habilitar_botones)

        self.setLayout(layout)

    def habilitar_botones(self):
        # Habilitar botones si el campo de texto no está vacío
        texto = self.nombreArchivo.text().strip()
        self.btnPDF.setEnabled(bool(texto))
        self.btnWORD.setEnabled(bool(texto))

    def realizar_opcion(self):
        boton_presionado = self.sender()
        nombre_archivo = self.nombreArchivo.text().strip()

        if boton_presionado.text() == "Guardar en formato pdf":
            extraccion(self.imagenProcesada,nombre_archivo,0)
            self.close()
        elif boton_presionado.text() == "Guardar en formato docx":
            extraccion(self.imagenProcesada,nombre_archivo,1)
            self.close()
