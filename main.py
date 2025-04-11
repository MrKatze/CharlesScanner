import cv2
from app import imageScanner
from app import cameraScanner

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