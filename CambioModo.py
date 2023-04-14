
from djitellopy import Tello
me = Tello()
me.connect()
# put the drone in AP mode, and give it the credentials of the router

ssid = "dron"
contraseña = "dron0000"
me.connect_to_wifi(ssid, contraseña)
print ('ya')
