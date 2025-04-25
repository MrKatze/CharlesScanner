#Scanner de Camara
import cv2
import numpy as np

#from app import utils
import utils
class cameraScanner: 
    def __init__(self,indexcamera=0):
        # Inicializa la cámara
        self.cap = cv2.VideoCapture(indexcamera) #Camara Laptop
        # Establecer resolución deseada
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.resolutionOutput =  utils.resolutionOutput 
        #Verifica si se abrió bien
        if not self.cap.isOpened():
            print("No se pudo abrir la cámara.")
            exit()
        pass

    def scan(self,show=False):
        try:
            ret, frame = self.cap.read()
            if not ret:
                print("No se pudo recibir el frame. Saliendo...")
                
            
            dst = utils.processImageCanny(frame,100,200,self.resolutionOutput,showcanny=show)
            if show:

                cv2.imshow('Camara sin efectos', frame)
                if not isinstance(dst, np.ndarray):
                    cv2.imshow('Camara con documento recortado', frame)
                else:
                    cv2.imshow('Camara con documento recortado', dst)
                    
            # cv2.imshow('Camara con efecto espejo', mirrored_frame)
            # cv2.imshow('Camara con contornos', cnts)
            return frame,dst
        except Exception as e:
            print("ha ocurrido un error:",e)
            # self.close()

    
    def close(self):

        # Libera recursos
        self.cap.release()
        cv2.destroyAllWindows()