#Archivo donde iran la gran mayoria de funciones que se usaran en el proyecto

import cv2
import numpy as np

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
    p1,p2,p3,p4 = pts[0], pts[1], pts[2], pts[3]
    # print("n_points=",n_points)
    print("n_points=",pts)
    print("n_points=",p1,p2,p3,p4)
    return None

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
            getResolutionOutput(points)
            # print("points=",points)
            cv2.circle(image, tuple(points[0]), 7, (255, 0, 0), 2)
            cv2.circle(image, tuple(points[1]), 7, (0, 255, 0), 2)
            cv2.circle(image, tuple(points[2]), 7, (0, 0, 255), 2)
            cv2.circle(image, tuple(points[3]), 7, (255, 255, 255), 2)

            width = ro[0]
            height = ro[1]  
            pts1 = np.float32(points)
            pts2 = np.float32([[0,0], [width,0],[0, height], [width, height]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            return cv2.warpPerspective(gray, matrix, (width, height))
        return 0
