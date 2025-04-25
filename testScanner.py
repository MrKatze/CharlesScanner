from app import imageScanner
import cv2
a = imageScanner.imageScanner("assets/test.jpeg")
# a = imageScanner.imageScanner("assets/test8.jpg")
a.scan(show=True)



