import asyncio
import random
import threading
import time

import websockets
from djitellopy import Tello, TelloSwarm
import cv2 as cv

# create handler for each connection

def video_stream ():
    global drone
    global sending_video_stream

    while True:
        if sending_video_stream:
            img = drone.get_frame_read().frame
            cv.imshow('frame', img)
            cv.waitKey(1)



async def handler(websocket, path):
    global cont
    global drone
    global connected
    global turn
    global numOp
    global sending_video_stream

    clients.append(websocket)

    while True:
        print ('waiting')
        message = await websocket.recv()
        print ('recibo :', message);
        splited = message.split("/")
        command = splited[1]

        if command == 'play':
            print('envio turno ', cont)
            await websocket.send('yourTurn/'+str(cont))

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

            num = splited[2]
            print('num ', num)

            if int(num) == turn and connected:

                if command == 'takeOff':
                    print('takeOff')

                    battery = drone.get_battery()
                    for client in clients:
                        await client.send('battery/' + str(battery))
                    drone.takeoff()

                    await websocket.send('volando')
                    numOp = random.randint(3, 6)


                elif command == 'GiraL':
                    print('GiraL')
                    drone.rotate_counter_clockwise(90)
                    await websocket.send('done')

                elif command == 'Adelante':
                    print('Adelante')
                    drone.move_forward(50)
                    await websocket.send('done')
                elif command == 'GiraR':
                    print('GiraR')
                    drone.rotate_clockwise(90)
                    await websocket.send('done')
                elif command == 'Izquierda':
                    print('izquierda')
                    drone.move_left(50)
                    await websocket.send('done')
                elif command == 'Flip':
                    print('Flip')
                    #drone.flip('l')
                    await websocket.send('done')
                elif command == 'Derecha':
                    print('Derecha')
                    drone.move_right(50)
                    await websocket.send('done')
                elif command == 'Arriba':
                    print('Arriba')
                    drone.move_up(50)
                    await websocket.send('done')
                elif command == 'Atras':
                    print('Atras')
                    drone.move_back(50)
                    await websocket.send('done')
                elif command == 'Abajo':
                    print('Abajo')
                    drone.move_down(50)
                    await websocket.send('done')

                elif command == 'land':
                    print('land')
                    drone.land()
                    for client in clients:
                        await client.send('onHearth')
                    connected = False
                    cont = 0

                if connected:
                    battery = drone.get_battery()
                    print ('battery ', battery)
                    for client in clients:
                        await client.send('battery/' + str(battery))
                    numOp = numOp - 1
                    print(numOp)
                    if numOp == 0:
                        numOp = random.randint(3, 6)
                        print ('nuevo nop ',numOp )
                        haveIt = False
                        while not haveIt:
                            new = random.randint(0, cont - 1)
                            if new != turn:
                                turn = new
                                haveIt = True
                        print('nuevo entre 0 y ', cont - 1)
                        print (turn)
                        for client in clients:
                            await client.send('newTurn/' + str(turn))



    #reply = f"Data recieved as:  {command}!"

    #await websocket.send(reply)



cont = 0
connected = False
numOp = 0
clients = []
drone = Tello()
drone.connect()
drone.streamon()
print ('conectado')


start_server = websockets.serve(handler, host="0.0.0.0", port= 8002)

asyncio.get_event_loop().run_until_complete(start_server)
print ('waiting')

asyncio.get_event_loop().run_forever()