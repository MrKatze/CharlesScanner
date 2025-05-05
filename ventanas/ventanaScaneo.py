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
from app.cameraScanner import cameraScanner
from datetime import datetime
import qtawesome as qta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_destino = os.path.join('documentos')

class VentanaEscaneo(QWidget):
    def __init__(self, ventana_principal=None):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.setWindowTitle("Escaneo")
        self.resize(800, 600)
        
        # Estilo general de la ventana
        self.setStyleSheet("""
            QWidget {
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
                border-radius: 5px;
                padding: 5px 10px;
            }
            QSlider {
                border: none;
                background: #e6e6e6;
                height: 10px;
            }
            QLabel {
                font-family: Arial, sans-serif;
                font-size: 12pt;
            }
        """)

        # Crear interruptor deslizable
         # Crear interruptor deslizable
        self.interruptor = InterruptorDeslizable()
        self.interruptor.estado_cambiado.connect(self.actualizar_estado_botones)

        self.slider_brillo = QSlider(Qt.Horizontal)
        self.slider_brillo.setRange(0, 100)
        self.slider_brillo.setValue(50)
        self.slider_brillo.valueChanged.connect(self.cambiar_brillo)
        self.slider_brillo.setVisible(False)
       

        self.slider_contraste = QSlider(Qt.Horizontal)
        self.slider_contraste.setRange(0, 100)
        self.slider_contraste.setValue(50)
        self.slider_contraste.valueChanged.connect(self.cambiar_contraste)
        self.slider_contraste.setVisible(False)
        # Etiquetas para los sliders
        self.etiqueta_brillo = QLabel(f"Brillo: {self.slider_brillo.value()}")
        self.etiqueta_contraste = QLabel(f"Contraste: {self.slider_contraste.value()}")
        self.etiqueta_brillo.setVisible(False)
        self.etiqueta_contraste.setVisible(False)

        # Etiquetas de imagen con estilo mejorado
        self.etiqueta_original = QLabel("Imagen original")
        self.etiqueta_original.setFixedSize(400, 300)
        self.etiqueta_original.setStyleSheet("""
            border: 1px solid #cfcfcf;
            padding: 10px;
            border-radius: 5px;
        """)

        self.etiqueta_escaneada = QLabel("Imagen escaneada")
        self.etiqueta_escaneada.setFixedSize(400, 300)
        self.etiqueta_escaneada.setStyleSheet("""
            border: 1px solid #cfcfcf;
            padding: 10px;
            border-radius: 5px;
        """)
        imagen_predeterminada = os.path.join(os.path.dirname(__file__), "..","recursos/assets","predeterminada.png")
        imagen_error = os.path.join(os.path.dirname(__file__), "..","recursos/assets","error.png")
        # Cargar imagen predeterminada
        self.imagen_predeterminada = QPixmap(imagen_predeterminada)
        self.imagen_error = QPixmap(imagen_error)
        self.etiqueta_original.setPixmap(self.imagen_predeterminada.scaled(self.etiqueta_original.width(),
                                                                      self.etiqueta_original.height(),
                                                                      Qt.KeepAspectRatio))
        self.etiqueta_escaneada.setPixmap(self.imagen_predeterminada.scaled(self.etiqueta_escaneada.width(),
                                                                       self.etiqueta_escaneada.height(),
                                                                       Qt.KeepAspectRatio))
        
        self.boton_seleccionar = QPushButton("Seleccionar Imagen")
        self.boton_seleccionar.setIcon(qta.icon('fa5s.image'))
        self.boton_seleccionar.clicked.connect(self.seleccionar_imagen)

        self.boton_scaneo = QPushButton("Escanear Imagen con cámara")
        self.boton_scaneo.setIcon(qta.icon('fa5s.camera'))
        self.boton_scaneo.clicked.connect(self.escanear_imagen)
        self.boton_scaneo.setEnabled(False)
        
        self.boton_procesar = QPushButton("Procesar Imagen")
        self.boton_procesar.setIcon(qta.icon('fa5s.spinner'))
        self.boton_procesar.clicked.connect(self.procesar_imagen)
        self.boton_procesar.setEnabled(False)  # Deshabilitado al inicio
        
        # Crear interfaz
        self.crear_interfaz()

    def actualizar_estado_botones(self, estado):
        """Habilita el botón de escaneo cuando el interruptor está activado"""
        self.boton_scaneo.setEnabled(estado)
        self.boton_seleccionar.setEnabled(not estado)
        print("Entro")
    def crear_interfaz(self):
        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)
        
        layout_principal.addWidget(self.interruptor)
        layout_principal.addWidget(self.etiqueta_brillo)
        layout_principal.addWidget(self.slider_brillo)
        layout_principal.addWidget(self.etiqueta_contraste)
        layout_principal.addWidget(self.slider_contraste)

        layout_apartados = QHBoxLayout()
        layout_botones = QHBoxLayout()
        layout_principal.addLayout(layout_apartados)
        layout_principal.addLayout(layout_botones)
        # Apartado para imágenes
        layout_apartados.addWidget(self.etiqueta_original)
        layout_apartados.addWidget(self.etiqueta_escaneada)
        
        # Añadir elementos al diseño principal
        layout_botones.addWidget(self.boton_seleccionar)
        layout_botones.addWidget(self.boton_scaneo)
        layout_botones.addWidget(self.boton_procesar)
            
    def tomar_foto_guardar(self, directorio_destino):
        cam = cv2.VideoCapture(0)

        if not cam.isOpened():
            print("No se pudo acceder a la cámara.")
            return

        print("Presiona ESPACIO para tomar la foto. ESC para salir.")

        while True:
            ret, frame = cam.read()
            if not ret:
                print("Error al capturar imagen.")
                break

            cv2.imshow("Presiona ESPACIO para capturar", frame)

            key = cv2.waitKey(1)
            if key == 27:  # ESC
                print("Cancelado.")
                break
            elif key == 32:  # ESPACIO
                # Generar nombre de archivo con timestamp
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                nombre_archivo = f"foto_{timestamp}.png"
                ruta_guardado = os.path.join(directorio_destino, nombre_archivo)

                cv2.imwrite(ruta_guardado, frame)
                print(f"Foto guardada en: {ruta_guardado}")
                break

        cam.release()
        cv2.destroyAllWindows()
            
    def escanear_imagen(self):
        print("Escaneando imagen...")
        print('PRUEBAAA 2, ruta: ', ruta_destino)
        self.tomar_foto_guardar(ruta_destino)
        self.seleccionar_imagen()

    def cambiar_brillo(self, valor):
        self.etiqueta_brillo.setText(f"Brillo: {valor}")
        
        print(f"Brillo ajustado a: {valor}")
        
    def cambiar_contraste(self, valor):
        self.etiqueta_contraste.setText(f"Contraste: {valor}")
        print(f"Contraste ajustado a: {valor}")

    def seleccionar_imagen(self):
        self.ruta_imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
        if self.ruta_imagen:
            print('PRUEBAAAAAA: ', self.ruta_imagen)
            self.boton_procesar.setEnabled(True)
            self.slider_brillo.setEnabled(True)
            self.slider_contraste.setEnabled(True)
            escaner = imageScanner(self.ruta_imagen)    
            imagen_original, imagen_procesada = escaner.scan()
            self.imagenProcesada = imagen_procesada

            # Validar imágenes antes de procesarlas
            if isinstance(imagen_original, (np.ndarray, cv2.UMat)) and isinstance(imagen_procesada, (np.ndarray, cv2.UMat)):
                self.mostrar_imagen(imagen_original, self.etiqueta_original)
                self.mostrar_imagen(imagen_procesada, self.etiqueta_escaneada)
            else:

                self.etiqueta_original.setPixmap(self.imagen_error.scaled(self.etiqueta_original.width(),
                                                                      self.etiqueta_original.height(),
                                                                      Qt.KeepAspectRatio))
                self.etiqueta_escaneada.setPixmap(self.imagen_error.scaled(self.etiqueta_escaneada.width(),
                                                                       self.etiqueta_escaneada.height(),
                                                                       Qt.KeepAspectRatio))
                self.boton_procesar.setEnabled(False)  # Deshabilitado al inicio
                print(f"Error: La imagen procesada no es válida. Valor recibido: {imagen_procesada}")

    # def seleccionar_imagen_camera(self):
    #     self.ruta_imagen, _ = 
    #     if self.ruta_imagen:
    #         print('PRUEBAAAAAA_camera: ', self.ruta_imagen)
    #         self.boton_procesar.setEnabled(True)
    #         self.slider_brillo.setEnabled(True)
    #         self.slider_contraste.setEnabled(True)
    #         escaner = imageScanner(self.ruta_imagen)
    #         imagen_original, imagen_procesada = escaner.scan()
    #         self.imagenProcesada = imagen_procesada

    #         # Validar imágenes antes de procesarlas
    #         if isinstance(imagen_original, (np.ndarray, cv2.UMat)) and isinstance(imagen_procesada, (np.ndarray, cv2.UMat)):
    #             self.mostrar_imagen(imagen_original, self.etiqueta_original)
    #             self.mostrar_imagen(imagen_procesada, self.etiqueta_escaneada)
    #         else:

    #             self.etiqueta_original.setPixmap(self.imagen_error.scaled(self.etiqueta_original.width(),
    #                                                                   self.etiqueta_original.height(),
    #                                                                   Qt.KeepAspectRatio))
    #             self.etiqueta_escaneada.setPixmap(self.imagen_error.scaled(self.etiqueta_escaneada.width(),
    #                                                                    self.etiqueta_escaneada.height(),
    #                                                                    Qt.KeepAspectRatio))
    #             self.boton_procesar.setEnabled(False)  # Deshabilitado al inicio
    #             print(f"Error: La imagen procesada no es válida. Valor recibido: {imagen_procesada}")


    def procesar_imagen(self):
        self.boton_procesar.setEnabled(False)
        tarjeta = VentanaGuardadoArchivo(self.imagenProcesada)
        tarjeta.exec_()
        

    def mostrar_imagen(self, image, label):
        """Convierte una imagen de OpenCV a formato Pixmap y la ajusta al QLabel manteniendo la proporción."""
        if not isinstance(image, np.ndarray):
            print(f"Error: Se esperaba una matriz pero se recibió {type(image)}")
            return
        
        if image.dtype != np.uint8:
            image = cv2.convertScaleAbs(image)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = image_rgb.shape
        bytes_per_line = channels * width
        q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))

    def abrirCamara():
        camera = cameraScanner(0)
        while True:
            camera.scan(show=True)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                camera.close()
                break