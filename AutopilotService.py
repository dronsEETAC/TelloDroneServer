import json
import math
import threading
import paho.mqtt.client as mqtt
import time
from djitellopy import Tello, TelloSwarm
from subprocess import Popen, PIPE
import subprocess

'''
These are the different values for the state of the autopilot:
    'connected' (only when connected the telemetry_info packet will be sent every 250 miliseconds)
    'arming'
    'armed'
    'disarmed'
    'takingOff'
    'flying'
    'returningHome'
    'landing'
    'onHearth'

The autopilot can also be 'disconnected' but this state will never appear in the telemetry_info packet 
when disconnected the service will not send any packet
'''
def get_telemetry_info ():
    global state
    telemetry_info = {
        'lat': 0,
        'lon': 0,
        'heading': 0,
        'groundSpeed': 0,
        'altitude': 0,
        'battery': 0,
        'state': state
    }
    return telemetry_info


def send_telemetry_info():
    global external_client
    global sending_telemetry_info
    global sending_topic

    while sending_telemetry_info:
        external_client.publish(sending_topic + "/telemetryInfo", json.dumps(get_telemetry_info()))
        time.sleep(0.25)




def process_message(message, client):
    global drone
    global swarm
    global direction
    global go
    global sending_telemetry_info
    global sending_topic
    global op_mode
    global sending_topic
    global state

    splited = message.topic.split("/")
    origin = splited[0]
    command = splited[2]
    print ('recibo ', command)
    sending_topic = "autopilotService/" + origin


    if command == "connect":
        print ('connect')
        drone.connect()
        state = 'connected'

        sending_telemetry_info = True
        y = threading.Thread(target=send_telemetry_info)
        y.start()



        #drone.connect()
    if command == "armDrone":

        state = 'armed'
    if command == "takeOff":
        drone.takeoff()
        state = 'flying'


    if command == "returnToLaunch":
        print ('land')

        drone.land()
        state = 'onHearth'

    if command == "go":
        direction = message.payload.decode("utf-8")
        print("Going ", direction)

        if direction == "North":
            drone.go_xyz_speed(50,0 ,0, 100)
        if direction == "South":
            drone.go_xyz_speed(-50, 0, 0, 100)
        if direction == "East":
            drone.go_xyz_speed(0, 50, 0, 100)
        if direction == "West":
            drone.go_xyz_speed(0, -50, 0, 100)
       





def on_external_message(client, userdata, message):
    global external_client
    process_message(message, external_client)

def ponStationMode ():

    me = Tello()
    me.connect()
    # put the drone in AP mode, and give it the credentials of the router
    ssid = "ICARUS_15_24"
    contraseña = "R3botado"
    ssid = "portatil_miguel"
    contraseña = "mimara1456."
    me.connect_to_wifi(ssid, contraseña)
    print ('ya')


def AutopilotService ():
    global external_client
    global drone
    global swarm

    #ponStationMode()
    '''
    swarm = TelloSwarm.fromIps(["192.168.137.75", "192.168.137.243"])
    for drone in swarm:
        drone.connect()
        print ('batery',  drone.get_battery())
        time.sleep(5)
    '''

    drone = Tello()
    #external_broker_address = "192.168.1.46"
    external_broker_address = "broker.hivemq.com"
    external_broker_port = 8000



    external_client = mqtt.Client("Autopilot_external", transport="websockets")
    #external_client = mqtt.Client("Autopilot_external")

    external_client.on_message = on_external_message
    external_client.connect(external_broker_address, external_broker_port)
    external_client.subscribe('+/autopilotService/#')
    #drone = Tello()
    print ('waiting...')
    external_client.loop_forever()


if __name__ == '__main__':

    AutopilotService()
