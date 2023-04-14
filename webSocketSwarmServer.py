import asyncio
import subprocess
import time

import websockets
from djitellopy import Tello, TelloSwarm
from EscuadronClass import Escuadron
'''
# create handler for each connection
def paso1 (i, tello):
    if (i == 0):
        tello.move_up (100)
        tello.move_back (400)
        tello.move_down (100)
    else:
        tello.move_forward (200)
    swarm.sync()
def paso2 (i, tello):
    if (i == 1):
        tello.move_up (100)
        tello.move_back (400)
        tello.move_down (100)
    else:
        tello.move_forward (200)
    swarm.sync()

def paso3 (i, tello):
    if (i == 2):
        tello.move_up (100)
        tello.move_back (400)
        tello.move_down (100)
    else:
        tello.move_forward (200)
    swarm.sync()

def final (i, tello):
    if (i == 2):
        tello.flip ('l')
    swarm.sync()
'''
async def handler(websocket, path):
    global escuadron
    while True:
        print ('waiting')
        command = await websocket.recv()
        print ('recibo :', command);
        if command == 'connect':

            print ('connect')

            escuadron = Escuadron()
            escuadron.CreaEscuadron()
            '''
            telloIPs = []
            out = subprocess.run(["arp", "-a"], check=True, capture_output=True, text=True).stdout
            res = out.split('\n')
            for w in res:
                if  '60-60-1f-5d-bd-4d' in w or \
                    '60-60-1f-fd-1b-ca' in w or \
                    '60-60-1f-d3-e4-5e' in w:
                    telloIPs.append (w.split()[0])
            print (telloIPs)
            swarm = TelloSwarm.fromIps(telloIPs)
            for drone in swarm:
                drone.connect()
                print('batery', drone.get_battery())
                time.sleep(2)
            '''
            await websocket.send('connected')

        elif command == 'takeOff':
            print ('takeOff')
            '''
            swarm.takeoff()
            swarm.parallel(lambda i, tello: tello.move_up(50))
            swarm.parallel(lambda i, tello: tello.move_forward(200))
            swarm.parallel(lambda i, tello: tello.rotate_counter_clockwise(90))
            time.sleep (5)
            swarm.parallel(lambda i, tello: tello.flip ('l'))
            swarm.parallel(lambda i, tello: tello.rotate_clockwise(90))
            swarm.parallel(lambda i, tello: tello.move_back(200))
            swarm.land()
            '''
            escuadron.takeOff()
            print ('flying)')
            await websocket.send('flying')


        elif command == 'land':
            print ('land')
            '''
            swarm.takeoff()
            swarm.parallel(paso1)
            print ('fin del paso 1')

            print ('vamos paso 2')
            swarm.parallel(lambda i, tello: tello.rotate_counter_clockwise(90))

            time.sleep(3)
            swarm.parallel(lambda i, tello: tello.rotate_clockwise(90))


            swarm.parallel(paso2)

            swarm.parallel(lambda i, tello: tello.rotate_counter_clockwise(90))
            time.sleep(3)
            swarm.parallel(lambda i, tello: tello.rotate_clockwise(90))


            swarm.parallel(paso3)

            swarm.parallel(lambda i, tello: tello.rotate_counter_clockwise(90))

            time.sleep(3)
            swarm.parallel(lambda i, tello: tello.rotate_clockwise(90))
            swarm.parallel(final)

            swarm.land()
            '''
            escuadron.land()
            await websocket.send('connected')

        elif command == 'forward':
            print ('forward')
            escuadron.goForward(0)
            await websocket.send('flying')
        elif command == 'back':
            print ('back')
            escuadron.goBack()
            await websocket.send('flying')
        elif command == 'rotateLeft':
            print ('rotateLeft')
            escuadron.rotateLeft()
            await websocket.send('flying')
        elif command == 'rotateRight':
            print ('rotateRight')
            escuadron.rotateRight()
            await websocket.send('flying')

        elif command == 'turnLeft':
            print('turnLeft')
            escuadron.goForward(1)
            await websocket.send('flying')
        elif command == 'turnRight':
            print ('turnRight')
            escuadron.goForward(2)
            await websocket.send('flying')





start_server = websockets.serve(handler, host="0.0.0.0", port= 8002)

asyncio.get_event_loop().run_until_complete(start_server)
print ('waiting')

asyncio.get_event_loop().run_forever()