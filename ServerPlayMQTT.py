import asyncio
import json
import random
import threading
import time

import websockets
from djitellopy import Tello, TelloSwarm

# create handler for each connection
import paho.mqtt.client as mqtt
import cv2 as cv

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
    #num = message.payload.decode("utf-8")

    if command == 'play':
        if cont < numPlayers:
            print('envio turno ', cont)
            mensaje = {
                'yourTurn': cont
            }
            client.publish('serverplay/yourTurn', json.dumps(mensaje))

            if not connected:
                print('connect')
                sending_video_stream = True
                y = threading.Thread(target=video_stream)
                y.start()

                connected = True
                turn = cont
                print('el turno es de ', turn)
            cont = cont + 1
        else:
            client.publish('serverplay/late')



    else:

        num = splited[2]
        print('num ', num)

        if int(num) == turn and connected:

            if command == 'takeOff':
                print('takeOff')

                battery = drone.get_battery()
                mensaje = {
                    'battery': battery
                }

                client.publish('serverplay/battery', json.dumps(mensaje))

                drone.takeoff()

                client.publish('serverplay/flying')
                numOp = random.randint(3, 6)


            elif command == 'GiraL':
                print('GiraL')
                drone.rotate_counter_clockwise(90)
                client.publish('serverplay/done')

            elif command == 'Adelante':
                print('Adelante')
                drone.move_forward(50)
                client.publish('serverplay/done')

            elif command == 'GiraR':
                print('GiraR')
                drone.rotate_clockwise(90)
                client.publish('serverplay/done')

            elif command == 'Izquierda':
                print('izquierda')
                drone.move_left(50)
                client.publish('serverplay/done')

            elif command == 'Flip':
                print('Flip')
                drone.flip('l')
                client.publish('serverplay/done')

            elif command == 'Derecha':
                print('Derecha')
                drone.move_right(50)
                client.publish('serverplay/done')

            elif command == 'Arriba':
                print('Arriba')
                drone.move_up(50)
                client.publish('serverplay/done')

            elif command == 'Atras':
                print('Atras')
                drone.move_back(50)
                client.publish('serverplay/done')

            elif command == 'Abajo':
                print('Abajo')
                drone.move_down(50)
                client.publish('serverplay/done')

            elif command == 'land':
                print('land')
                drone.land()

                client.publish('serverplay/onHearth')
                connected = False
                cont = 0

            if connected:
                battery = drone.get_battery()
                print('battery ', battery)

                battery = drone.get_battery()
                mensaje = {
                    'battery': battery
                }

                client.publish('serverplay/battery', json.dumps(mensaje))
                numOp = numOp - 1
                print(numOp)
                if numOp == 0:
                    numOp = random.randint(3, 6)
                    print('nuevo nop ', numOp)
                    haveIt = False
                    while not haveIt:
                        new = random.randint(0, cont - 1)
                        if new != turn:
                            turn = new
                            haveIt = True
                    print('nuevo entre 0 y ', cont - 1)
                    print(turn)
                    mensaje = {
                        'newTurn': turn
                    }

                    client.publish('serverplay/newTurn', json.dumps(mensaje))



def ServerRun(n):
    global cont
    global connected
    global numOp
    global numPlayers
    global drone

    numPlayers = n
    cont = 0
    connected = False
    numOp = 0
    drone = Tello()
    drone.connect()
    drone.streamon()
    print('conectado')

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