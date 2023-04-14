import paho.mqtt.client as mqtt

#external_broker_address = "broker.hivemq.com"

external_broker_address = "classpip.upc.edu"




external_broker_port = 8000

external_client = mqtt.Client("publisher", transport="websockets")
external_client.username_pw_set('dronsEETAC', 'mimara1456.')

external_client.connect(external_broker_address, external_broker_port)
external_client.publish('connect', 'hola')
print('ya')
