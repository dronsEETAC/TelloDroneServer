import cv2
from djitellopy import Tello
from time import sleep
# Conectar al dron Tello
tello = Tello()
tello.connect()

# Iniciar transmisión de video
tello.streamon()
#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


print ('empiezo a grabar')
# Leer y escribir cuadros de video hasta que se presione la tecla 'q'
while True:
        # Leer un cuadro de video
        #frame = tello.get_frame_read().frame


        '''gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)'''

        # Mostrar el cuadro de video
        #cv2.imshow('Video del dron', frame)
        #cv2.waitKey(1)


        img = tello.get_frame_read().frame
        cv2.imshow('frame', img)
        cv2.waitKey(1)



# Liberar los recursos

cv2.destroyAllWindows()
