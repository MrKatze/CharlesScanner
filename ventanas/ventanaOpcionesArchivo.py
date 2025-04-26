from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
from app.ExportacionPDF import convertir_docx_a_pdf

class VentanaOpcionesArchivos(QDialog):
    def __init__(self, nombre_archivo):
        super().__init__()
        self.setWindowTitle("")
       # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)  # Sin bordes ni decoraciones
       # self.setAttribute(Qt.WA_TranslucentBackground)  # Fondo translúcido
        self.setStyleSheet("""
            QDialog {
        background-color: #White; /* Un poco menos translúcido */
        border-radius: 15px;
        border: 1px solid #000000; /* Bordes más visibles */
    }
        """)
        self.nombre_archivo = nombre_archivo
        self.setFixedSize(200, 250)  # Tamaño fijo de la tarjeta

        # Crear el layout y botones
        layout = QVBoxLayout()
        self.agregar_botones(layout)
        self.setLayout(layout)

    def agregar_botones(self, layout):
        opciones = ["Subir a Drive Google", "Búsqueda Inteligente", "Exportación a PDF","Cerrar"]
        for opcion in opciones:
            boton = QPushButton(opcion)
            self.aplicar_estilo_boton(boton)
            if opcion in ["Subir a Drive Google", "Búsqueda Inteligente"]:  # Deshabilitar algunos botones
                 boton.setEnabled(False)
            boton.clicked.connect(self.realizar_opcion)
            layout.addWidget(boton)

    def aplicar_estilo_boton(self, boton):
        boton.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                color: #333;
                border: none;
                border-radius: 10px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        boton.setFixedSize(180, 40)

    def realizar_opcion(self):
        boton_presionado = self.sender()

        if boton_presionado.text() == "Editar":
                print("Abriendo Editor")  # Aquí podrías añadir la integración con OpenCV
        elif boton_presionado.text() == "Subir a Drive Google":
                print("subiendo")  # Acción para la otra opción
        elif boton_presionado.text() == "Búsqueda Inteligente":
                print("Buscando")  # Acción para la otra opción
        elif boton_presionado.text() == "Exportación a PDF":
                print("Exportacion a PDF")  # Acción para la otra opción
                # Dirección relativa al archivo Python actual
                direccion = os.path.join(os.path.dirname(__file__), "..", "documentos")
                
                # Ruta del archivo fuente y del archivo destino
                archivo_docx = os.path.join(direccion, self.nombre_archivo)
                archivo_pdf = os.path.join(direccion, f"{os.path.splitext(self.nombre_archivo)[0]}.pdf")
                
                print(archivo_docx)
                # Llamada a la función convertir_docx_a_pdf
                convertir_docx_a_pdf(archivo_docx, archivo_pdf)
                
                self.close()
        elif boton_presionado.text()=="Cerrar":
             self.close() 

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            dialog_rect = self.geometry()
            if not dialog_rect.contains(self.mapToGlobal(event.pos())):
                self.close()

    def focusOutEvent(self, event: QEvent):
        # Cerrar cuando pierda el foco
        self.close()
