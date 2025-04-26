import sys
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QSlider
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from app.imageScanner import imageScanner  
from recursos.InterruptorDeslizable import InterruptorDeslizable
from ventanas.ventanaGuardadoArchivo import VentanaGuardadoArchivo

class VentanaEscaneo(QWidget):
    def __init__(self, ventana_principal=None):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.setWindowTitle("Escaneo")
        self.resize(800, 600)
        
        # Crear interruptor deslizable
        self.interruptor = InterruptorDeslizable()
        
        self.slider_brillo = QSlider(Qt.Horizontal)
        self.slider_brillo.setRange(0, 100)
        self.slider_brillo.setValue(50)
        self.slider_brillo.valueChanged.connect(self.cambiar_brillo)
        
        self.slider_contraste = QSlider(Qt.Horizontal)
        self.slider_contraste.setRange(0, 100)
        self.slider_contraste.setValue(50)
        self.slider_contraste.valueChanged.connect(self.cambiar_contraste)
        
        # Etiquetas para los sliders
        self.etiqueta_brillo = QLabel(f"Brillo: {self.slider_brillo.value()}")
        self.etiqueta_contraste = QLabel(f"Contraste: {self.slider_contraste.value()}")

        # Etiquetas de imagen con tamaño fijo
        self.etiqueta_original = QLabel("Imagen original")
        self.etiqueta_original.setFixedSize(400, 300)
        self.etiqueta_original.setStyleSheet("border: 1px solid black; padding: 10px;")

        self.etiqueta_escaneada = QLabel("Imagen escaneada")
        self.etiqueta_escaneada.setFixedSize(400, 300)
        self.etiqueta_escaneada.setStyleSheet("border: 1px solid black; padding: 10px;")

        self.boton_seleccionar = QPushButton("Seleccionar Imagen")
        self.boton_seleccionar.clicked.connect(self.seleccionar_imagen)

        self.boton_scaneo = QPushButton("Escanear Imagen con camara")
        self.boton_scaneo.clicked.connect(self.escanear_imagen)
        self.boton_scaneo.setEnabled(False)
        
        self.boton_procesar = QPushButton("Procesar Imagen")
        self.boton_procesar.clicked.connect(self.procesar_imagen)
        self.boton_procesar.setEnabled(False)  # Deshabilitado al inicio

        
        # Crear interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)
        
        layout_principal.addWidget(self.interruptor)
        
        layout_principal.addWidget(self.etiqueta_brillo)
        layout_principal.addWidget(self.slider_brillo)
        layout_principal.addWidget(self.etiqueta_contraste)
        layout_principal.addWidget(self.slider_contraste)

        layout_apartados = QHBoxLayout()
        layout_principal.addLayout(layout_apartados)

        # Apartado para imágenes
        layout_apartados.addWidget(self.etiqueta_original)
        layout_apartados.addWidget(self.etiqueta_escaneada)
        
        # Añadir elementos al diseño principal
        layout_principal.addWidget(self.boton_seleccionar)
        layout_principal.addWidget(self.boton_scaneo)
        layout_principal.addWidget(self.boton_procesar)
        
    def escanear_imagen(self):
        print("jsj")

    def cambiar_brillo(self, valor):
        self.etiqueta_brillo.setText(f"Brillo: {valor}")
        print(f"Brillo ajustado a: {valor}")
        
    def cambiar_contraste(self, valor):
        self.etiqueta_contraste.setText(f"Contraste: {valor}")
        print(f"Contraste ajustado a: {valor}")

    def seleccionar_imagen(self):
        self.ruta_imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
        if self.ruta_imagen:
            self.boton_procesar.setEnabled(True)

            escaner = imageScanner(self.ruta_imagen)  # Llama a la función existente
            imagen_original, imagen_procesada = escaner.scan()  # Usa su resultado
            self.imagenProcesada=imagen_procesada
            # Validar imágenes antes de procesarlas
            if isinstance(imagen_original, (np.ndarray, cv2.UMat)) and isinstance(imagen_procesada, (np.ndarray, cv2.UMat)):
                self.mostrar_imagen(imagen_original, self.etiqueta_original)
                self.mostrar_imagen(imagen_procesada, self.etiqueta_escaneada)
            else:
                print(f"Error: La imagen procesada no es válida. Valor recibido: {imagen_procesada}")

    def procesar_imagen(self):
        tarjeta = VentanaGuardadoArchivo( self.imagenProcesada)
        tarjeta.exec_()
        self.boton_procesar.setEnabled(False)
        '''direccion = os.path.join(os.path.dirname(__file__), "..", "documentos")
        if direccion:
            print("Procesando la imagen escaneada...")
            extraccion(self.imagenProcesada)
            self.boton_procesar.setEnabled(False)
        else:
            print("No se ha procesado una imagen aún.")'''

    def mostrar_imagen(self, image, label):
        """Convierte una imagen de OpenCV a formato Pixmap y la ajusta al QLabel manteniendo la proporción."""
        if not isinstance(image, np.ndarray):
            print(f"Error: Se esperaba una matriz pero se recibió {type(image)}")
            return
        
        if image.dtype != np.uint8:
            image = cv2.convertScaleAbs(image)  # Convierte la imagen a uint8

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = image_rgb.shape
        bytes_per_line = channels * width
        q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))

