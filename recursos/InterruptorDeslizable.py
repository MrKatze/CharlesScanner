from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap
from PyQt5.QtWidgets import QWidget
import qtawesome as qta  # Importar QtAwesome

class InterruptorDeslizable(QWidget):
    estado_cambiado = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 20)  # Ajustar tamaño para incluir el ícono
        self.activado = False
        self.icono_activo = qta.icon('fa5s.camera').pixmap(16, 16)  # Ícono de cámara
        self.icono_inactivo = qta.icon('fa5s.image').pixmap(16, 16)  # Ícono de imagen

    def mousePressEvent(self, event):
        self.activado = not self.activado
        self.estado_cambiado.emit(self.activado)
        self.update()

    def paintEvent(self, event):
        ancho = self.width()
        alto = self.height()

        pincel = QPainter(self)
        pincel.setRenderHint(QPainter.Antialiasing)

        # Dibujar fondo del interruptor
        color_fondo = QColor("#4caf50") if self.activado else QColor("#ccc")
        pincel.setBrush(QBrush(color_fondo))
        pincel.drawRoundedRect(20, 0, ancho - 20, alto, alto / 2, alto / 2)

        # Dibujar círculo deslizante
        pincel.setBrush(QBrush(QColor("#fff")))
        radio = alto - 4
        x = ancho - radio - 2 if self.activado else 22
        pincel.drawEllipse(QRect(x, 2, radio, radio))

        # Dibujar ícono a la izquierda del interruptor
        icono = self.icono_activo if self.activado else self.icono_inactivo
        pincel.drawPixmap(2, 2, icono)

