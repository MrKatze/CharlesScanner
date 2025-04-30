import json
import os
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
import sys

class VentanaNotificacion(QDialog):
    CONFIG_FILE = "config.json"  # Archivo de configuración

    def __init__(self, nombre_archivo, tiempo_cierre=3000):  # Tiempo en milisegundos
        super().__init__()
        self.setWindowTitle("Notificación")
        self.setFixedSize(300, 100)
        self.nombre_archivo = nombre_archivo

        # Aplicar estilos tipo notificación emergente
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #555;
                box-shadow: 5px 5px 12px rgba(0, 0, 0, 0.3);
            }
            QLabel {
                font-family: Arial, sans-serif;
                font-size: 11pt;
                color: black;
                padding: 5px;
            }
        """)

        # Configuración del mensaje
        mensaje = "❌ Error al procesar" if self.nombre_archivo is None else "✅ Conversión Exitosa"
        self.label_ruta = QLabel(f"{mensaje}: {self.nombre_archivo}", self)
        self.label_ruta.setWordWrap(True)
        self.label_ruta.setAlignment(Qt.AlignCenter)

        # Diseño de la ventana
        layout = QVBoxLayout()
        layout.addWidget(self.label_ruta)
        self.setLayout(layout)

        # Configurar el temporizador para cerrar la ventana después del tiempo especificado
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close)
        self.timer.start(tiempo_cierre)  # Se activa el temporizador


