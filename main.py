import sys
import os
from PyQt5.QtWidgets import QApplication
from ventanas.ventanaPrincipal import VentanaPrincipal

#CAMARA
def camara():
    sc = cameraScanner.cameraScanner(0)
    print("Presiona 'q' para salir")
    while True:
        camaraOriginal,camaraRecortada = sc.scan(show=True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sc.close
            break

#IMAGEN
def imagen():
    # scannerImagen = imageScanner.imageScanner('assets/test.jpeg') 
    # scannerImagen = imageScanner.imageScanner('assets/test2.png') 
    scannerImagen = imageScanner.imageScanner('assets/test3.jpeg') 
    imagenOriginal, imagenRecortada =  scannerImagen.scan(show=True)
    
camara()
# imagen()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Lanza la ventana principal
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
