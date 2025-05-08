from PyQt5.QtWidgets import *
from ventanas.ventanaNotificacion import VentanaNotificacion
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

class VentanaBusquedaInteligente(QDialog):
    def __init__(self, file_path):
        super().__init__()
        self.setWindowTitle("Búsqueda Inteligente")
        self.resize(800, 600)

        self.file_path = file_path
        self.texto_documento = self.cargar_documento(file_path)

        # Cargar el modelo de spaCy en español
        try:
            self.nlp = spacy.load("es_core_news_sm")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el modelo de spaCy:\n{str(e)}")
            self.close()
            return

        # Layout principal
        layout_principal = QHBoxLayout()
        self.setLayout(layout_principal)

        # Panel lateral para categorías y barra de búsqueda
        panel_lateral = QVBoxLayout()
        layout_principal.addLayout(panel_lateral)

        # Lista de categorías encontradas
        self.lista_categorias = QListWidget()
        self.lista_categorias.itemClicked.connect(self.resaltar_categoria)
        panel_lateral.addWidget(QLabel("Categorías encontradas:"))
        panel_lateral.addWidget(self.lista_categorias)

        # Barra de búsqueda
        self.barra_busqueda = QLineEdit()
        self.barra_busqueda.setPlaceholderText("Buscar texto...")
        self.barra_busqueda.returnPressed.connect(self.buscar_texto_personalizado)
        panel_lateral.addWidget(QLabel("Buscar texto:"))
        panel_lateral.addWidget(self.barra_busqueda)

        # Área de texto para mostrar el documento
        self.area_texto = QTextEdit()
        self.area_texto.setReadOnly(True)
        self.area_texto.setText(self.texto_documento)
        layout_principal.addWidget(self.area_texto)

        # Botón para iniciar la búsqueda
        boton_buscar = QPushButton("Iniciar Búsqueda")
        boton_buscar.clicked.connect(self.iniciar_busqueda)
        panel_lateral.addWidget(boton_buscar)

        # Diccionario para almacenar los resultados de búsqueda
        self.resultados = {}

    def cargar_documento(self, file_path):
        """Carga el contenido del documento (PDF o DOCX)."""
        try:
            if file_path.endswith(".docx"):
                doc = Document(file_path)
                return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            elif file_path.endswith(".pdf"):
                text = []
                reader = PdfReader(file_path)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
                return "\n".join(text)
            else:
                QMessageBox.critical(self, "Error", "Formato de archivo no soportado.")
                self.close()
                return ""
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al leer el archivo:\n{str(e)}")
            return ""

    def iniciar_busqueda(self):
        """Usa NLP para detectar entidades (correos, teléfonos, etc.)."""
        doc = self.nlp(self.texto_documento)

        # Extraer entidades con spaCy
        self.resultados = {
            "Correos electrónicos": [ent.text for ent in doc.ents if ent.label_ == "EMAIL"],
            "Números de teléfono": [ent.text for ent in doc.ents if ent.label_ == "TELEFONO"],
            "CURP": [ent.text for ent in doc.ents if ent.label_ == "CURP"],
            "RFC": [ent.text for ent in doc.ents if ent.label_ == "RFC"],
        }

        # Respaldo con expresiones regulares para entidades no reconocidas por spaCy
        if not self.resultados["Correos electrónicos"]:
            self.resultados["Correos electrónicos"] = re.findall(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", self.texto_documento)
        if not self.resultados["Números de teléfono"]:
            self.resultados["Números de teléfono"] = re.findall(r"(\d{2}[- ]?){4}\d{2}", self.texto_documento)
        if not self.resultados["CURP"]:
            self.resultados["CURP"] = re.findall(r"[A-Z]{4}\d{6}[A-Z]{6}\d{2}", self.texto_documento)
        if not self.resultados["RFC"]:
            self.resultados["RFC"] = re.findall(r"[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}", self.texto_documento)

        # Filtrar resultados vacíos
        for categoria in list(self.resultados.keys()):
            if not self.resultados[categoria]:
                del self.resultados[categoria]

        # Actualizar la lista de categorías
        self.lista_categorias.clear()
        for categoria, resultados in self.resultados.items():
            if resultados:
                self.lista_categorias.addItem(f"{categoria} ({len(resultados)})")

        # Resaltar los resultados en el texto
        self.resaltar_resultados()

    def resaltar_resultados(self):
        """Resalta los resultados encontrados en el texto."""
        colores = {
            "Correos electrónicos": QColor("#FFF9C4"),  # Amarillo suave
            "Números de teléfono": QColor("#B3E5FC"),   # Cyan claro
            "CURP": QColor("#C8E6C9"),                  # Verde claro
            "RFC": QColor("#BBDEFB"),                   # Azul claro
            "Personalizado": QColor("orange"),          # Naranja
        }

        cursor = self.area_texto.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())  # Restablecer formato

        # Resaltar cada categoría
        for categoria, resultados in self.resultados.items():
            formato = QTextCharFormat()
            formato.setBackground(colores.get(categoria, QColor("white")))  # Color por categoría
            for texto in resultados:
                start_idx = 0
                while start_idx < len(self.texto_documento):
                    match = self.texto_documento.find(texto, start_idx)
                    if match == -1:
                        break
                    cursor.setPosition(match)
                    cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(texto))
                    cursor.mergeCharFormat(formato)
                    start_idx = match + len(texto)

    def resaltar_categoria(self, item):
        """Resalta solo los resultados de la categoría seleccionada."""
        categoria = item.text().split(" (")[0]
        if categoria in self.resultados:
            self.area_texto.selectAll()
            self.area_texto.setText(self.texto_documento)  # Restablecer el texto
            self.resaltar_resultados()  # Resaltar todo
            self.area_texto.find(self.resultados[categoria][0])  # Ir al primer resultado

    def buscar_texto_personalizado(self):
        """Busca texto personalizado ingresado por el usuario."""
        texto = self.barra_busqueda.text().strip()
        if not texto:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingresa un texto para buscar.")
            return

        # Buscar coincidencias del texto personalizado
        coincidencias = [m.group() for m in re.finditer(re.escape(texto), self.texto_documento, re.IGNORECASE)]

        if coincidencias:
            # Agregar la categoría "Personalizado" a los resultados
            self.resultados["Personalizado"] = coincidencias

            # Actualizar la lista de categorías
            self.lista_categorias.clear()
            for categoria, resultados in self.resultados.items():
                if resultados:
                    self.lista_categorias.addItem(f"{categoria} ({len(resultados)})")

            # Resaltar las coincidencias en el texto
            self.resaltar_resultados()
        else:
            QMessageBox.information(self, "Sin coincidencias", f"No se encontraron coincidencias para '{texto}'.")

    def copiar_al_portapapeles(self, texto):
        """Copia el texto seleccionado al portapapeles."""
        clipboard = QApplication.clipboard()
        clipboard.setText(texto)
        QMessageBox.information(self, "Copiado", f"'{texto}' copiado al portapapeles.")

