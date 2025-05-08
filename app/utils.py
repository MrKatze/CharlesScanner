#Archivo donde iran la gran mayoria de funciones que se usaran en el proyecto

import cv2
import numpy as np
import math
import re
from PyQt5.QtWidgets import QMessageBox

resolutionOutput =  [720,1080]

def sortPoints(pts):
    n_points = np.concatenate([pts[0], pts[1], pts[2], pts[3]]).tolist()
    # print("n_points=",n_points)
    y_order = sorted(n_points, key=lambda n_points: n_points[1])
    # print("y_order=",y_order)
    x1_order = y_order[:2]
    x1_order = sorted(x1_order, key=lambda n_points: n_points[0])
    # print("x1_order=",x1_order)
    x2_order = y_order[2:]
    x2_order = sorted(x2_order, key=lambda n_points: n_points[0])
    # print("x2_order=",x2_order)
    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]

def getResolutionOutput(pts):
    p1, p2, p3, p4 = pts[0], pts[1], pts[2], pts[3]
    
    # Calcular alturas de los lados izquierdo y derecho
    l1 = abs(p3[1] - p1[1])
    l2 = abs(p4[1] - p2[1])
    altura = (l1 + l2) / 2

    # Calcular anchos de los lados superior e inferior
    a1 = abs(p2[0] - p1[0])
    a2 = abs(p4[0] - p3[0])
    ancho = (a1 + a2) / 2

    # print(f"Ancho = {ancho}, Altura = {altura}")

    if altura == 0 or ancho == 0:
        print("Error: ancho o altura es cero")
        return None

    # Simplificar la relación
    gcd = math.gcd(int(ancho), int(altura))
    aspecto_ancho = int(ancho / gcd)
    aspecto_alto = int(altura / gcd)

    # print(f"Relación de aspecto detectada: {aspecto_ancho}:{aspecto_alto}")

    # Calcular nueva resolución para altura fija de 720 px
    altura_fija = 720
    ancho_calculado = int((aspecto_ancho / aspecto_alto) * altura_fija)

    # print(f"Resolución sugerida: {ancho_calculado}x{altura_fija}")

    return [ancho_calculado, altura_fija]


def processImageCanny(image, th1=20, th2=200, ro=resolutionOutput, showcanny=False):   

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    desenfocada = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(desenfocada, th1, th2,L2gradient=True)
    canny =cv2.dilate(canny, None,iterations=1)

    #Mustra los bordes en blanco y negro
    if showcanny:
        cv2.namedWindow("Canny", cv2.WINDOW_NORMAL)
        cv2.imshow('Canny', canny)
        cv2.namedWindow("Desenfocada", cv2.WINDOW_NORMAL)
        cv2.imshow('Desenfocada', desenfocada)

    cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]

    for c in cnts:
        epsilon = 0.1 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        if len(approx) == 4:
            cv2.drawContours(image, [approx], 0, (0, 255, 255), 2)
            # print("aprox=",approx)
            points = sortPoints(approx)
            width, height =getResolutionOutput(points)
            # print("points=",points)
            cv2.circle(image, tuple(points[0]), 7, (255, 0, 0), 2)
            cv2.circle(image, tuple(points[1]), 7, (0, 255, 0), 2)
            cv2.circle(image, tuple(points[2]), 7, (0, 0, 255), 2)
            cv2.circle(image, tuple(points[3]), 7, (255, 255, 255), 2)

            pts1 = np.float32(points)
            pts2 = np.float32([[0,0], [width,0],[0, height], [width, height]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            return cv2.warpPerspective(gray, matrix, (width, height))
        return 0

def buscar_texto_personalizado(self):
    """Busca texto personalizado ingresado por el usuario."""
    texto = self.barra_busqueda.text().strip()
    if not texto:
        QMessageBox.warning(self, "Advertencia", "Por favor, ingresa un texto para buscar.")
        return

    # Buscar coincidencias del texto personalizado
    coincidencias = [m.group() for m in re.finditer(re.escape(texto), self.texto_documento, re.IGNORECASE)]

    if coincidencias:
        # Agregar la categoría "Personalizado" a los resultados
        self.resultados["Personalizado"] = coincidencias

        # Actualizar la lista de categorías
        self.lista_categorias.addItem(f"Personalizado ({len(coincidencias)})")

        # Resaltar las coincidencias en el texto
        self.resaltar_resultados()
    else:
        QMessageBox.information(self, "Sin coincidencias", f"No se encontraron coincidencias para '{texto}'.")
