import json
import time

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from djitellopy import Tello, TelloSwarm

app = Flask(__name__)
CORS(app)

#from data import data

def moveForward(i, tello):
    global swarm
    swarm.go_xyz_speed(50, 0, 0, 100)
    swarm.sync()

@app.route('/connect', methods=['GET'])
def connect():
    global swarm
    print ('connect')
    swarm = TelloSwarm.fromIps([
        "192.168.137.21",
        "192.168.137.176",
        #  "192.168.137.89"
        # "192.168.137.218"
    ])
    for drone in swarm:
        drone.connect()
        print('batery', drone.get_battery())
        time.sleep(2)



    return jsonify({'response': 'connected'})

@app.route('/takeOff', methods=['GET'])
def takeOff():
    global swarm
    print ('takeOff')
    swarm.takeoff()

    return jsonify({'response': 'flying'})

@app.route('/land', methods=['GET'])
def land():
    global swarm
    print ('landing')
    swarm.land()
    return jsonify({'response': 'land'})

@app.route('/forward', methods=['GET'])
def formard():
    global swarm
    print ('formard')
    swarm.parallel(lambda i, tello: tello.move_forward(50))
    swarm.land()
    return jsonify({'response': 'formard'})

@app.route('/back', methods=['GET'])
def back():
    global swarm
    print ('back')
    swarm.parallel (lambda i , drone: drone.go_xyz_speed(-50, 0, 0, 100))
    return jsonify({'response': 'back'})


@app.route('/left', methods=['GET'])
def left():
    global swarm
    print ('left')
    swarm.parallel(lambda i, tello: tello.move_left(50))
    return jsonify({'response': 'left'})

@app.route('/right', methods=['GET'])
def right():
    global swarm
    print ('right')
    swarm.parallel (lambda i , drone: drone.go_xyz_speed(0, 50, 0, 100))
    return jsonify({'response': 'right'})



if __name__ == '__main__':
    print ('Starting API')
    # Load stored positions
    # we want to have the stored positions in a list (in memory)

    # start listening
    app.run(debug=True, host="0.0.0.0", port=4000)
