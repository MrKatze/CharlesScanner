from PyQt5.QtCore import Qt, QRect,pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout

class InterruptorDeslizable(QWidget):
    estado_cambiado = pyqtSignal(bool)  
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(25, 15)
        self.activado = False

    def mousePressEvent(self, event):
        self.activado = not self.activado
        self.estado_cambiado.emit(self.activado)  # Emitir señal al cambiar el estado
        self.update()
        print("Estado:", "Activado" if self.activado else "Desactivado")

    def paintEvent(self, event):
        ancho = self.width()
        alto = self.height()

        # Configurar el pintor
        pincel = QPainter(self)
        pincel.setRenderHint(QPainter.Antialiasing)

        # Dibujar el fondo del interruptor
        if self.activado:
            pincel.setBrush(QBrush(QColor("#4caf50")))  # Verde cuando está activado
        else:
            pincel.setBrush(QBrush(QColor("#ccc")))  # Gris cuando está desactivado
        pincel.drawRoundedRect(0, 0, ancho, alto, alto / 2, alto / 2)

        # Dibujar el círculo deslizante
        pincel.setBrush(QBrush(QColor("#fff")))  # Blanco para el círculo
        radio = alto - 4
        x = ancho - radio - 2 if self.activado else 2
        pincel.drawEllipse(QRect(x, 2, radio, radio))