import asyncio
import random
import time

import websockets
from djitellopy import Tello, TelloSwarm

# create handler for each connection

async def handler(websocket, path):

    clients.append(websocket)

    while True:
        print ('waiting')
        color = await websocket.recv()
        print ('recibo :', color);
        for client in clients:
            await client.send( color)


    #reply = f"Data recieved as:  {command}!"

    #await websocket.send(reply)



clients = []

start_server = websockets.serve(handler, host="0.0.0.0", port= 8002)

asyncio.get_event_loop().run_until_complete(start_server)
print ('waiting')

asyncio.get_event_loop().run_forever()