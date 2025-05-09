import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ventanas.ventanaVisualizacion import VentanaVisualizacion

def main():
    # Crear la aplicación de PyQt
    app = QApplication(sys.argv)

    # Ruta de la imagen de prueba
    ruta_imagen = "assets/prueba3.jpg"  # Cambia esto por la ruta de tu imagen

    # Cargar la imagen
    imagen = QImage(ruta_imagen)
    if imagen.isNull():
        print(f"Error: No se pudo cargar la imagen desde '{ruta_imagen}'.")
        return

    # Crear y mostrar la ventana de visualización
    ventana = VentanaVisualizacion(imagen)
    ventana.exec_()

    # Imprimir los puntos seleccionados
    print("Puntos seleccionados:")
    for punto in ventana.puntos:
        print(f"({punto.x()}, {punto.y()})")

if __name__ == "__main__":
    main()