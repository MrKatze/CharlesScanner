from PyQt5.QtWidgets import *
from ventanas.ventanaNotificacion import VentanaNotificacion
import qtawesome as qta
from PyQt5.QtCore import QSize, Qt
from app.google_drive import upload_to_drive
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class  VentanaOpcionesArchivos(QDialog):
    def __init__(self,nombre_archivo,tipo):
        super().__init__()
        self.setWindowTitle("Opciones")
        self.setGeometry(300, 200, 300, 200)

        self.nombre_archivo=nombre_archivo
        self.tipo=tipo        
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
        self.agregar_botones(layout)
        self.setLayout(layout)

        
        self.setLayout(layout)
    def agregar_botones(self, layout):
        opciones = ["Subir a Drive Google", "Búsqueda Inteligente", "Exportación a PDF"]
        iconos=["fa5s.folder","fa5s.search","fa5s.file-pdf"]
        for i, opcion in enumerate(opciones):
            if self.tipo == 0 and opcion == "Exportación a PDF":
                continue  # Saltar la creación de este botón si tipo es 0
            boton = QToolButton()
            boton.setText(opcion)
            boton.setIcon(qta.icon(iconos[i]))  
            boton.setIconSize(QSize(40, 40))
            boton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            boton.clicked.connect(self.realizar_opcion)
            layout.addWidget(boton)


    def realizar_opcion(self):
        file_path = os.path.join(BASE_DIR, 'documentos', self.nombre_archivo)
        boton_presionado = self.sender()

        if boton_presionado.text() == "Subir a Drive Google":
            # upload_to_drive(f'/documentos/{self.nombre_archivo}',self.nombre_archivo)
            upload_to_drive(file_path, self.nombre_archivo)
            
            print("Subiendo")  # Aquí podrías añadir la integración con OpenCV
        elif boton_presionado.text() == "Búsqueda Inteligente":
            print("Buscando")  # Acción para la otra opción
        elif boton_presionado.text() == "Exportación a PDF":
            tarjeta=VentanaNotificacion(self.nombre_archivo,0,5000);
            tarjeta.exec();
            self.close() 
            print("Exportando")  # Acción para la otra opcióndef realizar_opcion(self):
        file_path = os.path.join(BASE_DIR, 'documentos', self.nombre_archivo)
        boton_presionado = self.sender()

        if boton_presionado.text() == "Subir a Drive Google":
            try:
                upload_to_drive(file_path, self.nombre_archivo)

                QMessageBox.information(
                    self,
                    "Subida exitosa",
                    f"El archivo '{self.nombre_archivo}' se subió correctamente a Google Drive."
                )
                print("Subiendo")
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error al subir",
                    f"No se pudo subir el archivo.\n\nDetalle:\n{str(e)}"
                )
                print(f"Error al subir: {e}")

        elif boton_presionado.text() == "Búsqueda Inteligente":
            print("Buscando")

        elif boton_presionado.text() == "Exportación a PDF":
            tarjeta = VentanaNotificacion(self.nombre_archivo, 5000)
            tarjeta.exec()
            self.close()
            print("Exportando")
