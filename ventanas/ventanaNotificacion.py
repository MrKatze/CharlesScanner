import json
import os
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
import sys

class VentanaNotificacion(QDialog):
    CONFIG_FILE = "config.json"  # Archivo de configuración

    def __init__(self, nombre_archivo, tipo, tiempo_cierre=3000):  # Tiempo en milisegundos
        super().__init__()
        self.setWindowTitle("Notificación")
        self.setFixedSize(300, 100)
        self.nombre_archivo = nombre_archivo

        # Aplicar estilos tipo notificación emergente
        self.setStyleSheet("""
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ffffff, stop:1 #e6e6e6);
        border-radius: 12px;
        border: 2px solid #888;
        box-shadow: 6px 6px 15px rgba(0, 0, 0, 0.35);
    }
    QLabel {
        font-family: Arial, sans-serif;
        font-size: 12pt;
        font-weight: bold;
        color: #333;
        padding: 8px;
    }
""")

        # Configuración del mensaje
        if tipo==0:
            mensaje = f"❌ Error al procesar {self.nombre_archivo}" if self.nombre_archivo is None else "✅ Conversión Exitosa"
        if tipo==1:
            mensaje = "❌ Error al guardar {self.nombre_archivo}" if self.nombre_archivo is None else f"✅ Archivo {self.nombre_archivo} fue guardado exitosamente"
            
        
        self.label_ruta = QLabel(f"{mensaje}", self)
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


