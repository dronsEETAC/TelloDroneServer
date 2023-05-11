import asyncio
import json
import threading
import time

import websockets
from djitellopy import Tello, TelloSwarm
import cv2 as cv
import paho.mqtt.client as mqtt

# create handler for each connection

def video_stream ():
    global drone
    global sending_video_stream

    while True:
        if sending_video_stream:
            img = drone.get_frame_read().frame
            cv.imshow('frame', img)
            cv.waitKey(1)




def on_message(client, userdata, message):
    global cont
    global drone
    global connected
    global turn
    global numOp
    global sending_video_stream


    splited = message.topic.split("/")
    command = splited[1]



    if command == 'connect':
        drone.connect()
        drone.streamon()
        sending_video_stream = True
        y = threading.Thread(target=video_stream)
        y.start()
        client.publish('serverOneDrone/connected')
        connected = True

    elif command == 'disconnect':
        print('disconnect')
        sending_video_stream = False
        client.publish('serverOneDrone/waiting')

    elif command == 'takeOff':
        battery = drone.get_battery()
        mensaje = {
            'battery': battery
        }

        client.publish('serverOneDrone/battery', json.dumps(mensaje))

        drone.takeoff()

        client.publish('serverOneDrone/flying')


    elif command == 'GiraL':
        print('GiraL')
        drone.rotate_counter_clockwise(90)
        client.publish('serverOneDrone/done')

    elif command == 'Adelante':
        print('Adelante')
        drone.move_forward(50)
        client.publish('serverOneDrone/done')

    elif command == 'GiraR':
        print('GiraR')
        drone.rotate_clockwise(90)
        client.publish('serverOneDrone/done')

    elif command == 'Izquierda':
        print('izquierda')
        drone.move_left(50)
        client.publish('serverOneDrone/done')

    elif command == 'Flip':
        print('Flip')
        # drone.flip('l')
        client.publish('serverOneDrone/done')

    elif command == 'Derecha':
        print('Derecha')
        drone.move_right(50)
        client.publish('serverOneDrone/done')

    elif command == 'Arriba':
        print('Arriba')
        drone.move_up(50)
        client.publish('serverOneDrone/done')

    elif command == 'Atras':
        print('Atras')
        drone.move_back(50)
        client.publish('serverOneDrone/done')

    elif command == 'Abajo':
        print('Abajo')
        drone.move_down(50)
        client.publish('serverOneDrone/done')

    elif command == 'land':
        print('land')
        drone.land()

        client.publish('serverOneDrone/onHearth')


    if connected:
        battery = drone.get_battery()
        print('battery ', battery)

        battery = drone.get_battery()
        mensaje = {
            'battery': battery
        }

        client.publish('serverOneDrone/battery', json.dumps(mensaje))



def ServerRun():
    global connected

    global drone

    connected = False
    drone = Tello()


    external_broker_address = "broker.hivemq.com"
    external_broker_address = "classpip.upc.edu"
    external_broker_port = 8000

    external_client = mqtt.Client("Server play", transport="websockets")
    external_client.username_pw_set('dronsEETAC', 'mimara1456.')

    external_client.on_message = on_message
    external_client.connect(external_broker_address, external_broker_port)
    external_client.subscribe('movement/#')
    print('waiting...')
    external_client.loop_forever()

if __name__ == '__main__':
    ServerRun()