from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qtawesome as qta
import time
import os
from app.Extraer_texto import extraccion, conversionformato
from ventanas.ventanaNotificacion import VentanaNotificacion
class MedidorTiempo(QThread):
    progreso_actualizado = pyqtSignal(int)

    def __init__(self, imagenProcesada, nombre_archivo):
        super().__init__()
        self.imagenProcesada = imagenProcesada
        self.nombre_archivo = nombre_archivo

    def run(self):
        inicio = time.time()

        # Ejecutar la función de extracción
        self.texto_extraido, self.ruta_guardado = extraccion(self.imagenProcesada, self.nombre_archivo)

        fin = time.time()
        duracion = fin - inicio

        # Simulación de actualización progresiva basada en tiempo
        for i in range(101):
            porcentaje = min(100, int((i / 100) * (duracion / 5) * 100))
            self.progreso_actualizado.emit(porcentaje)
            time.sleep(duracion / 100)

        self.progreso_actualizado.emit(100)  # Finaliza en 100%

class VentanaGuardadoArchivo(QDialog):
    def __init__(self, ImagenProcesada):
        super().__init__()
        self.setWindowTitle("Opciones")
        self.setGeometry(500, 400, 500, 400)
        self.imagenProcesada = ImagenProcesada

        imagen_carga = os.path.join(os.path.dirname(__file__), "..", "recursos/assets", "779781883952778b25974baa3cf7679c.gif")
        
        # Crear QStackedWidget para alternar entre vistas (barra de carga y vista previa)
        self.stacked_widget = QStackedWidget(self)

        # Vista de barra de carga
        self.vista_barra_carga = QWidget()
        self.setup_vista_barra_carga(imagen_carga)

        # Vista de vista previa del texto
        self.vista_previa_texto = QWidget()
        self.setup_vista_previa_texto()
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
        
        # Agregar ambas vistas al stacked widget
        self.stacked_widget.addWidget(self.vista_barra_carga)
        self.stacked_widget.addWidget(self.vista_previa_texto)

        # Establecer la vista inicial como la de barra de carga
        self.stacked_widget.setCurrentWidget(self.vista_barra_carga)

        layout = QVBoxLayout()
        label = QLabel("Introduce el nombre del archivo:")
        layout.addWidget(label)

        # Configuración de los botones y campos de texto
        self.nombreArchivo = QLineEdit()
        layout.addWidget(self.nombreArchivo)

        layout.addWidget(self.stacked_widget)  # Agregar el stacked widget para la vista de carga o vista previa

        layout_botones = QHBoxLayout()
        layout.addLayout(layout_botones)
        
        self.btnCargarTexto = QPushButton("Extraer texto")
        self.btnCargarTexto.setEnabled(False)
        self.btnCargarTexto.setIcon(qta.icon('fa5s.arrow-alt-circle-down'))
        self.btnCargarTexto.clicked.connect(self.iniciar_extraccion_texto)
        layout_botones.addWidget(self.btnCargarTexto)

        self.btnPDF = QPushButton("Guardar en formato pdf")
        self.btnPDF.setEnabled(False)
        self.btnPDF.setIcon(qta.icon('fa5s.file-pdf'))
        self.btnPDF.clicked.connect(self.realizar_opcion)
        layout_botones.addWidget(self.btnPDF)

        self.btnWORD = QPushButton("Guardar en formato docx")
        self.btnWORD.setEnabled(False)
        self.btnWORD.setIcon(qta.icon('fa5s.file-word'))
        self.btnWORD.clicked.connect(self.realizar_opcion)
        layout_botones.addWidget(self.btnWORD)

        self.nombreArchivo.textChanged.connect(self.habilitar_botonExtraccion)
        self.setLayout(layout)

    def setup_vista_barra_carga(self, imagen_carga):
        # Vista de la barra de carga (con GIF y barra de progreso)
        layout = QVBoxLayout()
        
        # GIF de carga
        self.gif_carga = QLabel(self)
        self.gif_carga.setScaledContents(True) 
        self.gif_carga.setStyleSheet("""
    QLabel {
         border: 1px solid #cfcfcf;
         border-radius: 5px;
    }
""")
        self.movie = QMovie(imagen_carga)  # Asegúrate de colocar la ruta correcta
        self.gif_carga.setMovie(self.movie)
        layout.addWidget(self.gif_carga)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_bar)

        self.vista_barra_carga.setLayout(layout)

    def setup_vista_previa_texto(self):
        # Vista previa del texto extraído
        layout = QVBoxLayout()

        self.vistaPreviaTexto = QTextEdit()
        self.vistaPreviaTexto.setReadOnly(True)
        layout.addWidget(self.vistaPreviaTexto)

        self.vista_previa_texto.setLayout(layout)

    def iniciar_extraccion_texto(self):
        nombre_archivo = self.nombreArchivo.text().strip()
        self.movie.start()  # Iniciar animación
        if not nombre_archivo:
            return

        self.medidor_thread = MedidorTiempo(self.imagenProcesada, nombre_archivo)
        self.medidor_thread.progreso_actualizado.connect(self.progress_bar.setValue)
        self.medidor_thread.finished.connect(self.finalizar_extraccion)
        self.medidor_thread.start()

    def finalizar_extraccion(self):
        # Cambiar a la vista previa después de completar la extracción
        self.stacked_widget.setCurrentWidget(self.vista_previa_texto)

        texto_previo = self.medidor_thread.texto_extraido
        self.movie.stop()  # Detener animación
        if isinstance(texto_previo, list):
            texto_previo = "\n".join(texto_previo)

        self.vistaPreviaTexto.setText(texto_previo)
        self.habilitar_botones()

    def habilitar_botonExtraccion(self):
        self.btnCargarTexto.setEnabled(bool(self.nombreArchivo.text().strip()))

    def habilitar_botones(self):
        habilitar = bool(self.nombreArchivo.text().strip())
        self.btnPDF.setEnabled(habilitar)
        self.btnWORD.setEnabled(habilitar)
        self.btnCargarTexto.setEnabled(False)
    def realizar_opcion(self):
        boton_presionado = self.sender()
        nombre_archivo = self.nombreArchivo.text().strip()

        if boton_presionado.text() == "Guardar en formato pdf":
            indicador=conversionformato(self.medidor_thread.texto_extraido, nombre_archivo, self.medidor_thread.ruta_guardado, 0)
            if indicador==1:
                tarjeta=VentanaNotificacion(nombre_archivo,1,5000);
                tarjeta.exec();
            self.close()
        elif boton_presionado.text() == "Guardar en formato docx":
            indicador=conversionformato(self.medidor_thread.texto_extraido, nombre_archivo, self.medidor_thread.ruta_guardado, 1)
            if indicador==1:
                tarjeta=VentanaNotificacion(nombre_archivo,1,5000);
                tarjeta.exec();
            self.close()
            self.close()
