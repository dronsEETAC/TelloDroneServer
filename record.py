import cv2
from djitellopy import Tello
from time import sleep
# Conectar al dron Tello
tello = Tello()
tello.connect()

# Iniciar transmisión de video
tello.streamon()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Iniciar la conexión con el dron Tello
cap = cv2.VideoCapture('udp://0.0.0.0:11111')

# Verificar si la conexión con el dron está establecida
if not cap.isOpened():
    cap.open('udp://0.0.0.0:11111')


print ('preparo')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter('video_dron2.mp4', fourcc, 20.0, (960, 720))


print ('empiezo a grabar')
# Leer y escribir cuadros de video hasta que se presione la tecla 'q'
while True:
    # Leer un cuadro de video
    ret, frame = cap.read()

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Mostrar el cuadro de video
        cv2.imshow('Video del dron', frame)

        # Escribir el cuadro en el archivo de video
        output_video.write(frame)

        # Romper el bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Liberar los recursos
cap.release()
output_video.release()
cv2.destroyAllWindows()
