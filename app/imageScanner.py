#Escanneo realizao a partir de una imagen dada
#Scanner de Camara
import cv2
import numpy as np
import app.utils as utils

class imageScanner:
    ruta = None
    def __init__(self,ruta ):
        self.ruta = ruta
        #Resolucion de salida (resolutionOutput) 
        self.ro =  utils.resolutionOutput

        
    def scan(self,show=False):
        #Imagen Original
        image = cv2.imread(self.ruta)
        #Imagen Recortada
        dst = utils.processImageCanny(image,th1=20, th2=100, ro=self.ro , showcanny=show)
        
        # Mostrar en pantalla
        if show:
            print("Presiona 'q' para salir")
            cv2.namedWindow("Camara sin efectos", cv2.WINDOW_NORMAL)
            cv2.imshow('Camara sin efectos', image)
            # cv2.namedWindow("Escaneo",cv2.WINDOW_NORMAL)
            cv2.imshow('Escaneo', dst)
        #cv2.imshow('Camara sin efectos', image)
        #cv2.imshow('Escaneo', dst)

        # cv2.imshow('Camara con efecto espejo', mirrored_image)
        # cv2.imshow('Camara con contornos', cnts)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        return image, dst
    
