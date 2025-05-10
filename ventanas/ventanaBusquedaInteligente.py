from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QListWidget, QLineEdit, QTextEdit, QPushButton, QMessageBox, QLabel
from PyQt5.QtGui import QColor, QTextCharFormat, QTextCursor
from PyPDF2 import PdfReader
from docx import Document
import spacy
import re

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
        panel_lateral.addWidget(QLabel("Buscar texto:"))
        panel_lateral.addWidget(self.barra_busqueda)

        # Botón para la búsqueda personalizada
        boton_busqueda_personalizada = QPushButton("Buscar Personalizado")
        boton_busqueda_personalizada.clicked.connect(self.buscar_texto_personalizado)
        panel_lateral.addWidget(boton_busqueda_personalizada)

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