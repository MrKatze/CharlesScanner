from PyQt5.QtWidgets import *
from ventanas.ventanaNotificacion import VentanaNotificacion
from ventanas.ventanaBusquedaInteligente import VentanaBusquedaInteligente
import qtawesome as qta
from PyQt5.QtCore import QSize, Qt
from app.google_drive import upload_to_drive
import os
import re
from PyQt5.QtGui import QColor, QTextCharFormat, QTextCursor
from docx import Document
from PyPDF2 import PdfReader
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QListWidget, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtWidgets import QApplication
import spacy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class VentanaOpcionesArchivos(QDialog):
    def __init__(self, nombre_archivo, tipo):
        super().__init__()
        self.setWindowTitle("Opciones")
        self.setGeometry(300, 200, 300, 200)

        self.nombre_archivo = nombre_archivo
        self.tipo = tipo        
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
        iconos = ["fa5s.folder", "fa5s.search", "fa5s.file-pdf"]
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
            file_path = os.path.join(BASE_DIR, 'documentos', self.nombre_archivo)
            ventana_busqueda = VentanaBusquedaInteligente(file_path)
            ventana_busqueda.exec()   
        elif boton_presionado.text() == "Exportación a PDF":
            tarjeta = VentanaNotificacion(self.nombre_archivo, 5000)
            tarjeta.exec()
            self.close()
            print("Exportando")

    def alternar_modo(self):
        """Alterna entre modo oscuro y modo claro."""
        if self.boton_modo.property("modo") == "oscuro":
            # Cambiar a modo claro
            self.setStyleSheet("""
                QMainWindow {
                    background-color: white;
                }
                QWidget {
                    background-color: white;
                    border: 1px solid #cfcfcf;
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
                QLineEdit {
                    background-color: #F5F5F5;
                    border: 2px solid #87CEEB;
                    border-radius: 10px;
                    padding: 8px;
                    font-size: 14px;
                    color: #333;
                }
                QLineEdit:focus {
                    border: 2px solid #4682B4;
                    background-color: #FFFFFF;
                }
                QListWidget {
                    background-color: #FFFFFF;
                    border: 1px solid #DDDDDD;
                    border-radius: 10px;
                    color: black;
                }
                QLabel {
                    font-family: Arial, sans-serif;
                    font-size: 12pt;
                    color: black;
                }
            """)
            self.actualizar_estilo_menu_lateral("claro")
            self.actualizar_estilo_lista_archivos("claro")
            self.boton_modo.setIcon(qta.icon('fa5s.moon', color='black'))  # Cambiar ícono a luna
            self.boton_modo.setProperty("modo", "claro")
        else:
            # Cambiar a modo oscuro
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #121212;
                }
                QWidget {
                    background-color: #121212;
                    border: 1px solid #333333;
                }
                QPushButton {
                    background-color: #1E88E5;
                    color: white;
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #1565C0;
                }
                QPushButton:disabled {
                    background-color: #424242;
                    color: #BDBDBD;
                }
                QLineEdit {
                    background-color: #424242;
                    border: 2px solid #1E88E5;
                    border-radius: 10px;
                    padding: 8px;
                    font-size: 14px;
                    color: white;
                }
                QLineEdit:focus {
                    border: 2px solid #1565C0;
                    background-color: #616161;
                }
                QListWidget {
                    background-color: #212121;
                    border: 1px solid #424242;
                    border-radius: 10px;
                    color: white;
                }
                QLabel {
                    font-family: Arial, sans-serif;
                    font-size: 12pt;
                    color: white;
                }
            """)
            self.actualizar_estilo_menu_lateral("oscuro")
            self.actualizar_estilo_lista_archivos("oscuro")
            self.boton_modo.setIcon(qta.icon('fa5s.sun', color='yellow'))  # Cambiar ícono a sol
            self.boton_modo.setProperty("modo", "oscuro")

    def actualizar_estilo_menu_lateral(self, modo):
        """Actualiza los colores del menú lateral según el modo."""
        for i in range(self.layout_principal.count()):
            widget = self.layout_principal.itemAt(i).widget()
            if widget and isinstance(widget, QWidget):  # Verifica si es un widget
                if modo == "oscuro":
                    widget.setStyleSheet("""
                        background-color: #121212;
                        color: white;
                    """)
                else:
                    widget.setStyleSheet("""
                        background-color: white;
                        color: black;
                    """)

    def actualizar_estilo_lista_archivos(self, modo):
        """Actualiza los colores de los elementos de la lista de archivos según el modo."""
        for i in range(self.lista_archivos.count()):
            item = self.lista_archivos.item(i)
            if item.text().startswith(">"):  # Es un encabezado de subcarpeta
                if modo == "oscuro":
                    item.setForeground(QColor("white"))  # Texto blanco
                    item.setBackground(QColor("#333333"))  # Fondo gris oscuro
                else:
                    item.setForeground(QColor("black"))  # Texto negro
                    item.setBackground(QColor("#DCDCDC"))  # Fondo gris claro
            else:  # Es un archivo
                if modo == "oscuro":
                    item.setForeground(QColor("gray"))  # Texto blanco
                    item.setBackground(QColor("#212121"))  # Fondo gris oscuro
                else:
                    item.setForeground(QColor("black"))  # Texto negro
                    item.setBackground(QColor("#FFFFFF"))  # Fondo blanco

    

