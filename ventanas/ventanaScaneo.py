from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from app.imageScanner import imageScanner  

class VentanaEscaneo(QWidget):
    def __init__(self, ventana_principal=None):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.setWindowTitle("Escaneo")
        self.resize(800, 600)

        # Etiquetas de imagen con tamaño fijo
        self.etiqueta_original = QLabel("Imagen original")
        self.etiqueta_original.setFixedSize(400, 300)
        self.etiqueta_original.setStyleSheet("border: 1px solid black; padding: 10px;")

        self.etiqueta_escaneada = QLabel("Imagen escaneada")
        self.etiqueta_escaneada.setFixedSize(400, 300)
        self.etiqueta_escaneada.setStyleSheet("border: 1px solid black; padding: 10px;")

        self.boton_seleccionar = QPushButton("Seleccionar Imagen")
        self.boton_seleccionar.clicked.connect(self.seleccionar_imagen)

        # Crear interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)

        layout_apartados = QHBoxLayout()
        layout_principal.addLayout(layout_apartados)

        # Apartado para imágenes
        layout_apartados.addWidget(self.etiqueta_original)
        layout_apartados.addWidget(self.etiqueta_escaneada)

        layout_principal.addWidget(self.boton_seleccionar)

    def seleccionar_imagen(self):
        ruta_imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
        if ruta_imagen:
#            print(f"Imagen seleccionada: {ruta_imagen}")

            escaner = imageScanner(ruta_imagen)  # Llama a la función existente
            imagen_original, imagen_procesada = escaner.scan()  # Usa su resultado


            # Validar imágenes antes de procesarlas
            if isinstance(imagen_original, (np.ndarray, cv2.UMat)) and isinstance(imagen_procesada, (np.ndarray, cv2.UMat)):
                self.mostrar_imagen(imagen_original, self.etiqueta_original)
                self.mostrar_imagen(imagen_procesada, self.etiqueta_escaneada)
            else:
                print(f"Error: La imagen procesada no es válida. Valor recibido: {imagen_procesada}")

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
