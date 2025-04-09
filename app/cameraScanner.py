#Scanner de Camara
import cv2
import numpy as np

from app import utils
class cameraScanner: 
    def __init__(self,indexcamera=0):
        # Inicializa la cámara
        self.cap = cv2.VideoCapture(indexcamera) #Camara Laptop
        #Verifica si se abrió bien
        if not self.cap.isOpened():
            print("No se pudo abrir la cámara.")
            exit()
        pass

    def scan(self):
        print("Presiona 'q' para salir")

        while True:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    print("No se pudo recibir el frame. Saliendo...")
                    break
                dst = utils.processImage(frame,showcanny=True)
                cv2.imshow('Camara sin efectos', frame)
                if not isinstance(dst, np.ndarray):
                    cv2.imshow('Camara con documento recortado', frame)
                else:
                    cv2.imshow('Camara con documento recortado', dst)
                    
                # cv2.imshow('Camara con efecto espejo', mirrored_frame)
                # cv2.imshow('Camara con contornos', cnts)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.close
                    break
            except Exception as e:
                print("ha ocurrido un error:",e)
                # self.close()
                break

    def close(self):

        # Libera recursos
        self.cap.release()
        cv2.destroyAllWindows()