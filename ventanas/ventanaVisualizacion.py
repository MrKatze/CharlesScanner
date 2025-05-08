from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPointF
import cv2

class VentanaVisualizacion(QDialog):
    def __init__(self, imagen, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Visualización de Imagen")
        self.resize(800, 600)

        # Configurar la imagen
        self.imagen = imagen
        self.pixmap = QPixmap.fromImage(imagen)
        self.puntos = []  # Lista para almacenar los puntos seleccionados

        # Configurar la escena y la vista
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.scene.addPixmap(self.pixmap)

        # Configurar el diseño
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        # Habilitar zoom y arrastre
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        # Conectar eventos
        self.view.wheelEvent = self.zoom_event
        self.scene.mousePressEvent = self.mouse_press_event

    def zoom_event(self, event):
        """Controla el zoom con el scroll del mouse."""
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.view.scale(factor, factor)

    def mouse_press_event(self, event):
        """Registra los puntos seleccionados al hacer clic en la imagen."""
        if len(self.puntos) < 4:  # Limitar a 4 puntos
            punto = self.view.mapToScene(event.scenePos().toPoint())
            self.puntos.append(punto)
            self.dibujar_punto(punto)

            if len(self.puntos) == 4:
                self.close()  # Cerrar la ventana cuando se seleccionen los 4 puntos

    def dibujar_punto(self, punto):
        """Dibuja un punto en la escena."""
        pen = QPen(Qt.red)
        pen.setWidth(5)
        self.scene.addEllipse(punto.x() - 2, punto.y() - 2, 4, 4, pen)