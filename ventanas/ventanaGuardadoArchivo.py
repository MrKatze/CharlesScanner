from PyQt5.QtWidgets import *
from app.Extraer_texto import extraccion
from PyQt5.QtCore import Qt
from app.Extraer_texto import conversionformato
import qtawesome as qta
class VentanaGuardadoArchivo(QDialog):
    def __init__(self, ImagenProcesada):
        super().__init__()
        self.setWindowTitle("Opciones")
        self.setGeometry(500, 400, 500, 400)
        self.imagenProcesada = ImagenProcesada

        # Agregar un borde visible al diálogo

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
                           
             QPushButton:disabled {
                background-color: #e6e6e6;
                color: #a0a0a0;
                border-radius: 5px;
                padding: 5px 10px;
            }
                           
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #cfcfcf;
                border-radius: 5px;
                padding: 5px;
            }
            QLabel, QPushButton, QLineEdit, QTextEdit {
                font-family: Arial, sans-serif;
                font-size: 12pt;
            }
        """)

        layout = QVBoxLayout()

        label = QLabel("Introduce el nombre del archivo:")
        layout.addWidget(label)

        # Campo de entrada para el nombre de archivo
        self.nombreArchivo = QLineEdit()
        layout.addWidget(self.nombreArchivo)
        
         # Campo de visualización de texto extraído
        self.vistaPreviaTexto = QTextEdit()
        self.vistaPreviaTexto.setReadOnly(True)  # Para que no sea editable
        layout.addWidget(self.vistaPreviaTexto)
        

        layout_botones = QHBoxLayout()
        layout.addLayout(layout_botones)
        # Botón para cargar el texto extraído en el campo de visualización
        self.btnCargarTexto = QPushButton("Extraer texto")
        self.btnCargarTexto.setEnabled(False)
        self.btnCargarTexto.setIcon(qta.icon('fa5s.arrow-alt-circle-down'))
        self.btnCargarTexto.clicked.connect(self.cargar_texto)
        layout_botones.addWidget(self.btnCargarTexto)

        # Botón para guardar en formato PDF
        self.btnPDF = QPushButton("Guardar en formato pdf")
        self.btnPDF.setEnabled(False)  # Desactivado inicialmente
        self.btnPDF.setIcon(qta.icon('fa5s.file-pdf'))
        self.btnPDF.clicked.connect(self.realizar_opcion)
        layout_botones.addWidget(self.btnPDF)

        # Botón para guardar en formato DOCX
        self.btnWORD = QPushButton("Guardar en formato docx")
        self.btnWORD.setEnabled(False)  # Desactivado inicialmente
        self.btnWORD.setIcon(qta.icon('fa5s.file-word'))
        self.btnWORD.clicked.connect(self.realizar_opcion)
        layout_botones.addWidget(self.btnWORD)

        # Conexión para habilitar botones cuando se ingrese texto
        self.nombreArchivo.textChanged.connect(self.habilitar_botonExtraccion)


         # Agregar la casilla de verificación para activar la contraseña
       # self.checkBoxContrasena = QCheckBox("Activar contraseña")
       # self.checkBoxContrasena.setEnabled(False)  # Inicialmente deshabilitada
       # self.checkBoxContrasena.stateChanged.connect(self.activar_contrasena)
      #  layout.addWidget(self.checkBoxContrasena)

        # Campo de entrada para la contraseña (deshabilitado por defecto)
      #  self.campoContrasena = QLineEdit()
       # self.campoContrasena.setEchoMode(QLineEdit.Password)  # Ocultar la contraseña mientras se escribe
      #  self.campoContrasena.setEnabled(False)  # Desactivado inicialmente
       # layout.addWidget(QLabel("Introduce una contraseña:"))
       # layout.addWidget(self.campoContrasena)

        self.setLayout(layout)
    
    def activar_contrasena(self, estado):
        # Habilitar/deshabilitar el campo de contraseña según la casilla
        if estado == Qt.Checked:  # Si la casilla está marcada
            self.campoContrasena.setEnabled(True)
        else:  # Si la casilla está desmarcada
            self.campoContrasena.setEnabled(False)

    def cargar_texto(self):
        # Extraer texto de la imagen procesada
        nombre_archivo = self.nombreArchivo.text().strip()
        self.texto_extraido,self.ruta_guardado= extraccion(self.imagenProcesada,nombre_archivo)
        texto_previo=self.texto_extraido
        # Verificar si el texto extraído es una lista y convertirlo a cadena
        if isinstance(texto_previo, list):
            texto_previo = "\n".join(texto_previo)  # Unir elementos de la lista con saltos de línea
        # Mostrar el texto en la vista previa
        self.vistaPreviaTexto.setText(texto_previo)
        self.habilitar_botones()

    def habilitar_botonExtraccion(self):
        # Habilitar botones si el campo de texto no está vacío
        texto = self.nombreArchivo.text().strip()
        self.btnCargarTexto.setEnabled(bool(texto))

    def habilitar_botones(self):
        # Habilitar botones si el campo de texto no está vacío
        texto = self.nombreArchivo.text().strip()
        habilitar = bool(texto)  # Comprobar si hay texto ingresado
        self.btnPDF.setEnabled(bool(texto))
        self.btnWORD.setEnabled(bool(texto))
        #self.checkBoxContrasena.setEnabled(habilitar) 
    
    def realizar_opcion(self):
        boton_presionado = self.sender()
        nombre_archivo = self.nombreArchivo.text().strip()
      #  contrasena = self.campoContrasena.text().strip() if self.campoContrasena.isEnabled() else None
        #print(contrasena)
        if boton_presionado.text() == "Guardar en formato pdf":
           # texto_extraido,ruta_guardado=extraccion(self.imagenProcesada,nombre_archivo)
            conversionformato(self.texto_extraido,nombre_archivo,self.ruta_guardado,0)
            self.close()
        elif boton_presionado.text() == "Guardar en formato docx":
         #   texto_extraido,ruta_guardado=extraccion(self.imagenProcesada,nombre_archivo)
            conversionformato(self.texto_extraido,nombre_archivo,self.ruta_guardado,1)
            #extraccion(self.imagenProcesada,nombre_archivo,1)
            self.close()
