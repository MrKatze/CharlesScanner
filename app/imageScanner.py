#Escanneo realizao a partir de una imagen dada#Scanner de Camara
import cv2
import numpy as np
import app.utils as utils
class imageScanner:
    ruta = None
    def __init__(self,ruta ):
        self.ruta = ruta
        
    def scan(self):
        print("Presiona 'q' para salir")
        image = cv2.imread(self.ruta)

        dst = utils.processImage(image)
        
        # Efecto espejo
        mirrored_image = cv2.flip(image, 1)

        # Mostrar en pantalla
        cv2.imshow('Camara sin efectos', image)
        cv2.imshow('Escaneo', dst)

        # cv2.imshow('Camara con efecto espejo', mirrored_image)
        # cv2.imshow('Camara con contornos', cnts)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    