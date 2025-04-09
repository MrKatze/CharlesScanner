import cv2
from app import imageScanner
from app import cameraScanner

#CAMARA
# sc = cameraScanner.cameraScanner()
# sc.scan()

#IMAGEN
# # scannerImagen = imageScanner.imageScanner('assets/test.jpeg') 
# # scannerImagen = imageScanner.imageScanner('assets/test2.png') 
scannerImagen = imageScanner.imageScanner('assets/test3.jpeg') 
scannerImagen.scan()