import asyncio
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
    global drone
    global sending_video_stream
    while True:
        print ('waiting')
        command = await websocket.recv()
        print ('recibo :', command);
        if command == 'connect':
            print ('connect')

            sending_video_stream = True
            y = threading.Thread(target=video_stream)
            y.start()
            await websocket.send('connected')
        elif command == 'disconnect':
            print ('disconnect')
            sending_video_stream = False
            await websocket.send('waiting')

        elif command == 'takeOff':
            print ('takeOff')
            drone.takeoff()
            await websocket.send('flying')

        elif command == 'GiraL':
            print('GiraL')
            drone.rotate_counter_clockwise(90)
            await websocket.send('done')
        elif command == 'Adelante':
            print ('Adelante')
            drone.move_forward(100)
            await websocket.send('done')
        elif command == 'GiraR':
            print('GiraR')
            drone.rotate_clockwise(90)
            await websocket.send('done')
        elif command == 'Izquierda':
            print('izquierda')
            drone.move_left(100)
            await websocket.send('done')
        elif command == 'Flip':
            print('Flip')
            #drone.flip('l')
        elif command == 'Derecha':
            print('Derecha')
            drone.move_right(100)
            await websocket.send('done')
        elif command == 'Arriba':
            print('Arriba')
            drone.move_up(100)
            await websocket.send('done')
        elif command == 'Atras':
            print('Atras')
            drone.move_back(100)
            await websocket.send('done')
        elif command == 'Abajo':
            print('Abajo')
            drone.move_down(50)
            await websocket.send('done')

        elif command == 'land':
            print('land')
            drone.land()
            #sending_video_stream = False
            await websocket.send('onHearth')

        await websocket.send('battery/'+str(drone.get_battery()))

    #reply = f"Data recieved as:  {command}!"

    #await websocket.send(reply)

drone = Tello()
drone.connect()
drone.streamon()
start_server = websockets.serve(handler, host="0.0.0.0", port= 8002)

asyncio.get_event_loop().run_until_complete(start_server)
print ('waiting')

asyncio.get_event_loop().run_forever()