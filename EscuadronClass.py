import subprocess
import time

from djitellopy import TelloSwarm, tello

class Escuadron:
    def CreaEscuadron(self):
        # detectar IPs, crear Swarm y conectar uno a uno
        #ips = ["147.93.119.2", "147.93.119.3", "147.93.119.4", "147.93.119.2", "147.93.119.3", "147.93.119.4"]
        telloIPs = []
        out = subprocess.run(["arp", "-a"], check=True, capture_output=True, text=True).stdout
        res = out.split('\n')
        for w in res:
            if '60-60-1f-5d-bd-4d' in w or \
                    '60-60-1f-fd-1b-ca' in w or \
                    '60-60-1f-d3-e4-5e' in w or \
                    '60-60-1f-dc-28-6c' in w:
                telloIPs.append(w.split()[0])
        print (telloIPs)
        self.swarm = TelloSwarm.fromIps(telloIPs)
        for drone in self.swarm:
            drone.connect()
            print('batery', drone.get_battery())
            time.sleep(2)
        self.n = len(telloIPs)

        '''Direction:
        0 => forward
        1 => turn left
        2 => turn right
        '''
        self.direction = []
        self.direction = [0 for i in range(self.n)]
        self.orientation = 0



    def goForward(self, turn):
        if abs(self.orientation) == 0:

            self.direction = [turn] + self.direction[0:-1]
            print('paso 1', self.direction)
            self.swarm.parallel(self.__turn)
            print('ya he girado', self.direction)
            self.swarm.parallel(self.__formward)
            print('avanzamos', self.direction)
        elif abs(self.orientation) == 2:
            self.direction = self.direction[1:] + [turn]
            self.swarm.parallel(self.__turn)
            self.swarm.parallel(self.__formward)
        elif turn == 0:
            self.swarm.parallel(lambda i, tello: tello.move_forward(100))

    def goBack(self, ):
        if abs(self.orientation) == 0:
            self.swarm.parallel(self.__back)
            self.swarm.parallel(self.__turnBack)
            self.direction = self.direction[1:] + [0]
        elif abs(self.orientation) == 2:
            self.swarm.parallel(self.__back)
            self.swarm.parallel(self.__turnBack)
            self.direction = [0] + self.direction[0:-1]
        else:
            self.swarm.parallel(lambda i, tello: tello.move_back(100))

    def rotateLeft(self):
        if sum(self.direction) == 0:
            self.swarm.parallel(lambda i, drone: drone.rotate_counter_clockwise(90))

        self.orientation = self.orientation - 1

    def rotateRight(self):
        if sum(self.direction) == 0:
            self.swarm.parallel(lambda i, drone: drone.rotate_clockwise(90))
        self.orientation = self.orientation + 1

    def takeOff(self):
        self.swarm.takeoff()

    def land(self):
        self.swarm.land()
        self.direction = []
        self.direction = [0 for i in range(self.n)]
        self.orientation = 0

    def __turn(self, i, tello):
        if self.direction[i] == 1:
            tello.rotate_counter_clockwise(90)
        elif self.direction[i] == 2:
            tello.rotate_clockwise(90)
        self.swarm.sync()

    def __turnBack(self, i, tello):
        if self.direction[i] == 1:
            tello.rotate_clockwise(90)
        elif self.direction[i] == 2:
            tello.rotate_counter_clockwise(90)
        self.swarm.sync()

    def __formward(self, i, tello):
        tello.move_forward(100)
        self.swarm.sync()

    def __back(self, i, tello):
        tello.move_back(100)
        self.swarm.sync()




