#Scanner de Camara
import cv2

# Inicializa la cámara
cap = cv2.VideoCapture(0) #Camara Laptop
# cap = cv2.VideoCapture(2) #Camara WebCam

# Verifica si se abrió bien
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()

print("Presiona 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        print("No se pudo recibir el frame. Saliendo...")
        break

    # Efecto espejo
    mirrored_frame = cv2.flip(frame, 1)

    # Redimensionar a 1920x1080
    #resized_frame = cv2.resize(mirrored_frame, (1920,1080))

    # Redimensionar a 1080x720
    resized_frame = cv2.resize(mirrored_frame, (1080,720))

    # Mostrar en pantalla
    cv2.imshow('Camara con efecto espejo (1920x1080)', resized_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera recursos
cap.release()
cv2.destroyAllWindows()