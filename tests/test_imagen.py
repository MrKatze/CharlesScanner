import sys
import os

import cv2
import numpy as np
import pytest
from app import utils

def create_test_image():
    # Create a blank image with a white rectangle
    img = np.zeros((500, 500, 3), dtype=np.uint8)
    cv2.rectangle(img, (100, 100), (400, 400), (255, 255, 255), -1)
    return img

def create_blank_image():
    # Imagen completamente negra
    return np.zeros((500, 500, 3), dtype=np.uint8)

def test_crop_document_found():
    image = create_test_image()
    # cv2.namedWindow("Imagen con rectangulo", cv2.WINDOW_NORMAL)
    # cv2.imshow("Imagen con rectangulo",image)
    # cv2.waitKey(0)
    cropped = utils.processImageCanny(image)

    assert cropped is not None, "Debería encontrar un documento para recortar"
    

def test_crop_document_not_found():
    image = create_blank_image()
    # cv2.namedWindow("Imagen sin rectangulo", cv2.WINDOW_NORMAL)
    # cv2.imshow("Imagen sin rectangulo",image)
    # cv2.waitKey(0)
    cropped = utils.processImageCanny(image)

    assert cropped is None, "No debería encontrar documentos en una imagen vacía"
    