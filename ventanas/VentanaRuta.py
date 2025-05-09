import json
import os
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
import sys
class VentanaSeleccionarRuta(QDialog):
    CONFIG_FILE = "config.json"  # Archivo de configuración

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seleccionar Ruta de Guardado")
        self.setFixedSize(300, 200)
        # Aplicar estilos generales
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #cfcfcf;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3);
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #e6e6e6;
                color: #a0a0a0;
            }
            QLabel {
                font-family: Arial, sans-serif;
                font-size: 12pt;
            }
        """)
        # Cargar ruta desde archivo de configuración o usar predeterminada
        self.ruta_default = os.path.expanduser("~/Documentos")  # Ruta predeterminada
        self.ruta_actual = self.cargar_ruta()  # Ruta actual (cargada)

        # Etiqueta para mostrar la ruta
        self.label_ruta = QLabel(f"Ruta actual: {self.ruta_actual}", self)
        self.label_ruta.setWordWrap(True)

        # Botones
        self.boton_cambiar_ruta = QPushButton("Cambiar", self)
        self.boton_cambiar_ruta.clicked.connect(self.cambiar_ruta)

        self.boton_restaurar_default = QPushButton("Restablecer", self)
        self.boton_restaurar_default.clicked.connect(self.restaurar_ruta_default)
        
        '''self.boton_guardar = QPushButton("Guardar", self)
        self.boton_guardar.clicked.connect(self.guardar_archivo)
        self.boton_guardar.setEnabled(False)'''
        # Layout
        layout=QVBoxLayout()
        layout.addWidget(self.label_ruta)
        #layout = QHBoxLayout()
        layout.addWidget(self.boton_cambiar_ruta)
        layout.addWidget(self.boton_restaurar_default)
        #layout.addWidget(self.boton_guardar)
        self.setLayout(layout)

    def cargar_ruta(self):
        """Cargar la ruta desde el archivo de configuración"""
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as file:
                config = json.load(file)
                return config.get("ruta_guardado", self.ruta_default)
        return self.ruta_default

    def guardar_ruta(self):
        """Guardar la ruta actual en el archivo de configuración"""
        with open(self.CONFIG_FILE, "w") as file:
            json.dump({"ruta_guardado": self.ruta_actual}, file)

    def cambiar_ruta(self):
        """Abrir cuadro de diálogo para seleccionar directorio"""
        nueva_ruta = QFileDialog.getExistingDirectory(self, "Seleccionar Directorio", self.ruta_actual)
        if nueva_ruta:  # Si el usuario selecciona una ruta
            self.ruta_actual = nueva_ruta
            self.label_ruta.setText(f"Ruta actual: {self.ruta_actual}")
            self.guardar_ruta()

    def restaurar_ruta_default(self):
        """Restaurar la ruta a la predeterminada"""
        self.ruta_actual = self.ruta_default
        self.label_ruta.setText(f"Ruta actual: {self.ruta_actual}")
        self.guardar_ruta()

    def guardar_archivo(self):
        """Ejemplo de guardar archivo en la ruta seleccionada"""
        archivo_ejemplo = os.path.join(self.ruta_actual, "archivo_ejemplo.txt")
        with open(archivo_ejemplo, "w") as archivo:
            archivo.write("Este es un archivo de ejemplo.")
        print(f"Archivo guardado en: {archivo_ejemplo}")



