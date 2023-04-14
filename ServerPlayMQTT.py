import asyncio
import json
import random
import threading
import time

import websockets
from djitellopy import Tello, TelloSwarm

# create handler for each connection
import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    global cont
    global drone
    global connected
    global turn
    global numOp


    splited = message.topic.split("/")
    command = splited[1]
    #num = message.payload.decode("utf-8")


    if command == 'play':
        print ('envio turno ', cont)
        mensaje = {
            'yourTurn': cont
        }
        client.publish('serverplay/yourTurn',json.dumps(mensaje))

        if not connected:
            print('connect')
            drone = Tello()
            drone.connect()
            connected = True
            turn = cont
            print('el turno es de ', turn)
        cont = cont + 1


    else:

        num = splited[2]
        print('num ', num)


        if int(num) == turn and connected:

            if command == 'takeOff':
                print ('takeOff')
                drone.takeoff()

            elif command == 'GiraL':
                print('GiraL')
                drone.rotate_counter_clockwise(90)
            elif command == 'Adelante':
                print ('Adelante')
                drone.move_forward(50)
            elif command == 'GiraR':
                print('GiraR')
                drone.rotate_clockwise(90)
            elif command == 'Izquierda':
                print('izquierda')
                drone.move_left(50)
            elif command == 'Flip':
                print('Flip')
                #drone.flip('l')
            elif command == 'Derecha':
                print('Derecha')
                drone.move_right(50)
            elif command == 'Arriba':
                print('Arriba')
                drone.move_up(50)
            elif command == 'Atras':
                print('Atras')
                drone.move_back(50)
            elif command == 'Abajo':
                print('Abajo')
                drone.move_down(50)

            elif command == 'land':
                print('land')
                drone.land()
            numOp = numOp + 1
            print (numOp)
            if numOp == 2:
                numOp = 0;
                print ('nuevo entre 0 y ', cont -1)
                turn=random.randint(0, cont -1)
                print ('nuevo turno ', turn)
                mensaje = {
                    'newTurn': turn
                }
                client.publish('serverplay/newTurn',json.dumps(mensaje))

def ServerPlay():
    global cont
    global connected
    global numOp


    cont = 0
    connected = False
    numOp = 0

    external_broker_address = "broker.hivemq.com"
    external_broker_port = 8000

    external_client = mqtt.Client("Server play", transport="websockets")

    external_client.on_message = on_message
    external_client.connect(external_broker_address, external_broker_port)
    external_client.subscribe('movement/#')
    print('waiting...')
    external_client.loop_forever()

if __name__ == '__main__':
    ServerPlay()