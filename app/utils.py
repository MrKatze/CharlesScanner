#Archivo donde iran la gran mayoria de funciones que se usaran en el proyecto

import cv2
import numpy as np

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

def processImage(image,showcanny=False):   

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 10, 100)
    canny =cv2.dilate(canny, None,iterations=1)
    if showcanny:
        cv2.imshow('Canny', canny)
    cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]

    for c in cnts:
        epsilon = 0.01 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        if len(approx) == 4:
            cv2.drawContours(image, [approx], 0, (0, 255, 255), 2)
            # print("aprox=",approx)
            points = sortPoints(approx)
            # print("points=",points)
            cv2.circle(image, tuple(points[0]), 7, (255, 0, 0), 2)
            cv2.circle(image, tuple(points[1]), 7, (0, 255, 0), 2)
            cv2.circle(image, tuple(points[2]), 7, (0, 0, 255), 2)
            cv2.circle(image, tuple(points[3]), 7, (255, 255, 255), 2)

            pts1 = np.float32(points)
            pts2 = np.float32([[0,0], [270,0],[0,310], [270,310]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            return cv2.warpPerspective(gray, matrix, (270, 310))
        return 0

