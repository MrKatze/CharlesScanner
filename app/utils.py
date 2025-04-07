#Archivo donde iran la gran mayoria de funciones que se usaran en el proyecto

import cv2

def listar_camaras(max_dispositivos=10):
    disponibles = []
    for i in range(0,max_dispositivos):
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:  # Si puede leer desde la cámara
            disponibles.append(i)
            cap.release()
    return disponibles

camaras = listar_camaras()
print("Cámaras disponibles:", camaras)
