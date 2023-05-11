import subprocess
import os, re

from djitellopy import Tello, TelloSwarm


def ponStationMode ():

    me = Tello()
    me.connect()
    # put the drone in AP mode, and give it the credentials of the router

    ssid = "dron"
    contraseña = "dron0000"
    me.connect_to_wifi(ssid, contraseña)
    print ('ya')

def SearchTellos():
    out = subprocess.run(["arp", "-a"], check = True, capture_output = True, text = True).stdout
    res = out.split ('\n')
    print ('out: ', out)
    print('res: ', res)
    telloIPs = []
    for w in res:
        if '60-60-1f-5d-bd-4d' in w or \
                '60-60-1f-d3-e4-5e' in w or \
                '60-60-1f-dc-32-88' in w :

            print (w.split()[0])
            telloIPs.append(w.split()[0])

    print (telloIPs)
    swarm = TelloSwarm.fromIps(telloIPs)

    swarm.connect()
    swarm.takeoff()
    swarm.land()





SearchTellos ()
'''
    tellos = []

    for each_line in scan_out_lines:

        split_line = [e for e in each_line.split(" ") if e != ""]

        if 'TELLO' in split_line[0]:
            tellos.append(split_line[0])

    # include drones in the table (label to identify drone and button to put it in AP mode

    for i in range(0, len(tellos)):
        name_lab1 = tk.Label(tellosFrame, text=tellos[i], width=10, justify='left', bg='white')

        name_lab1.grid(row=i + 1, column=0)

        b = Button(tellosFrame, text="put in AP mode", width=150, bg='red', fg="white",
                   command=partial(PutAPMode, i + 1))

        b.grid(row=i + 1, column=1)
    '''

'''
swarm = TelloSwarm.fromIps([
    "192.168.137.246",
    "192.168.137.90"
])

swarm.connect()
swarm.takeoff()

# run in parallel on all tellos
# 同时在所有Tello上执行


# run by one tello after the other
# 让Tello一个接一个执行
swarm.parallel(lambda i, tello: tello.move_forward(50))

# making each tello do something unique in parallel
# 让每一架Tello单独执行不同的操作
swarm.parallel(lambda i, tello: tello.move_left(50))

swarm.land()
swarm.end()
'''