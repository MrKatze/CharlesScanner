from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene, QPushButton, QSlider, QLabel
from PyQt5.QtGui import QPixmap, QPen, QCursor, QImage
from PyQt5.QtCore import Qt, QLineF
import cv2
import numpy as np

class VentanaVisualizacion(QDialog):
    def __init__(self, imagen, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Visualización de Imagen")
        self.imagen_original = imagen
        self.imagen_actual = imagen
        self.pixmap = QPixmap.fromImage(imagen)
        self.puntos = []  # Lista para almacenar los puntos seleccionados
        self.linea_guia = None  # Línea guía temporal

        # Establecer un tamaño fijo para la ventana
        self.resize(800, 600)

        # Configurar la escena y la vista
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.scene.addPixmap(self.pixmap)

        # Cambiar el cursor a crosshair
        self.view.setCursor(QCursor(Qt.CrossCursor))

        # Configurar el diseño principal
        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)

        # Añadir la vista de la imagen
        self.layout_principal.addWidget(self.view)

        # Añadir controles de ajustes
        self.crear_controles_ajustes()

        # Añadir texto flotante
        self.texto_flotante = QLabel("Presiona E para colocar una esquina", self)
        self.texto_flotante.setStyleSheet("color: white; background-color: black; padding: 5px;")
        self.texto_flotante.setAlignment(Qt.AlignCenter)
        self.texto_flotante.setGeometry(10, 10, 300, 30)  # Posición y tamaño del texto flotante

        # Habilitar zoom y arrastre
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        # Conectar eventos
        self.view.wheelEvent = self.zoom_event

    def crear_controles_ajustes(self):
        """Crea los controles para ajustar brillo, contraste y recorte."""
        layout_controles = QVBoxLayout()

        # Slider de brillo
        self.slider_brillo = QSlider(Qt.Horizontal)
        self.slider_brillo.setRange(-100, 100)
        self.slider_brillo.setValue(0)
        self.slider_brillo.valueChanged.connect(self.ajustar_brillo)
        layout_controles.addWidget(QLabel("Brillo"))
        layout_controles.addWidget(self.slider_brillo)

        # Slider de contraste
        self.slider_contraste = QSlider(Qt.Horizontal)
        self.slider_contraste.setRange(-100, 100)
        self.slider_contraste.setValue(0)
        self.slider_contraste.valueChanged.connect(self.ajustar_contraste)
        layout_controles.addWidget(QLabel("Contraste"))
        layout_controles.addWidget(self.slider_contraste)

        # Añadir los controles al diseño principal
        self.layout_principal.addLayout(layout_controles)

    def ajustar_brillo(self, valor):
        """Ajusta el brillo de la imagen."""
        imagen_cv = self.qimage_a_cv2(self.imagen_original)
        imagen_ajustada = cv2.convertScaleAbs(imagen_cv, alpha=1, beta=valor)
        self.actualizar_imagen(imagen_ajustada)

    def ajustar_contraste(self, valor):
        """Ajusta el contraste de la imagen."""
        imagen_cv = self.qimage_a_cv2(self.imagen_original)
        alpha = 1 + (valor / 100.0)  # Escalar contraste
        imagen_ajustada = cv2.convertScaleAbs(imagen_cv, alpha=alpha, beta=0)
        self.actualizar_imagen(imagen_ajustada)

    def iniciar_seleccion_esquinas(self):
        """Inicia la fase de selección de esquinas."""
        self.slider_brillo.setEnabled(False)
        self.slider_contraste.setEnabled(False)
        self.view.setDragMode(QGraphicsView.NoDrag)  # Deshabilitar el modo de arrastre
        self.view.viewport().setCursor(QCursor(Qt.CrossCursor))  # Cambiar el cursor a una cruceta
        self.scene.mousePressEvent = self.mouse_press_event  # Conectar el evento de clic a la escena

    def mouse_press_event(self, event):
        """Registra los puntos seleccionados al hacer clic en la imagen."""
        # Convertir la posición del clic a coordenadas de la escena
        punto = event.scenePos()
        self.puntos.append(punto)  # Agregar el punto a la lista
        self.dibujar_punto(punto)  # Dibujar el punto rojo

        # Dibujar la línea guía o cerrar el rectángulo
        if len(self.puntos) > 1:
            self.dibujar_linea_permanente(self.puntos[-2], self.puntos[-1])  # Línea entre los últimos dos puntos

        if len(self.puntos) == 4:
            # Cerrar el rectángulo
            self.dibujar_linea_permanente(self.puntos[-1], self.puntos[0])  # Línea entre el último y el primer punto
            self.close()  # Cerrar la ventana una vez seleccionados los 4 puntos

    def dibujar_punto(self, punto):
        """Dibuja un punto en la escena."""
        pen = QPen(Qt.red)
        pen.setWidth(5)
        self.scene.addEllipse(punto.x() - 2, punto.y() - 2, 4, 4, pen)

    def dibujar_linea_permanente(self, punto_inicio, punto_fin):
        """Dibuja una línea permanente entre dos puntos."""
        pen = QPen(Qt.yellow)
        pen.setWidth(2)
        self.scene.addLine(QLineF(punto_inicio, punto_fin), pen)

    def actualizar_imagen(self, imagen_cv):
        """Actualiza la imagen mostrada en la vista."""
        self.imagen_actual = self.cv2_a_qimage(imagen_cv)
        self.pixmap = QPixmap.fromImage(self.imagen_actual)
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)

    def zoom_event(self, event):
        """Controla el zoom con el scroll del mouse."""
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.view.scale(factor, factor)

    def keyPressEvent(self, event):
        """Captura la tecla presionada para colocar una esquina."""
        if event.key() == Qt.Key_E:
            # Obtener la posición actual del cursor en la escena
            cursor_pos = self.view.mapToScene(self.view.viewport().mapFromGlobal(QCursor.pos()))
            self.puntos.append(cursor_pos)  # Agregar el punto a la lista
            self.dibujar_punto(cursor_pos)  # Dibujar el punto rojo

            # Dibujar la línea guía o cerrar el rectángulo
            if len(self.puntos) > 1:
                self.dibujar_linea_permanente(self.puntos[-2], self.puntos[-1])  # Línea entre los últimos dos puntos

            if len(self.puntos) == 4:
                # Cerrar el rectángulo
                self.dibujar_linea_permanente(self.puntos[-1], self.puntos[0])  # Línea entre el último y el primer punto
                self.close()  # Cerrar la ventana una vez seleccionados los 4 puntos

    @staticmethod
    def qimage_a_cv2(qimage):
        """Convierte una QImage a una imagen de OpenCV."""
        qimage = qimage.convertToFormat(QImage.Format.Format_RGB32)
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.bits()
        ptr.setsize(height * width * 4)
        arr = np.array(ptr, dtype=np.uint8).reshape((height, width, 4))
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

    @staticmethod
    def cv2_a_qimage(cv_image):
        """Convierte una imagen de OpenCV a QImage."""
        height, width, channel = cv_image.shape
        bytes_per_line = 3 * width
        qimage = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        return qimage