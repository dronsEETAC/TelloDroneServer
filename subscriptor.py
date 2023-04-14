import paho.mqtt.client as mqtt


def on_message(client, userdata, message):

    if message.topic == 'connect':
        print ('connected')
        print ('payload ', message.payload)

#external_broker_address = "broker.hivemq.com"
external_broker_address = "classpip.upc.edu"
external_broker_port = 8000

external_client = mqtt.Client("subscriber", transport="websockets")

external_client.on_message = on_message
external_client.username_pw_set('dronsEETAC', 'mimara1456.')

external_client.connect(external_broker_address, external_broker_port)
external_client.subscribe('connect')
print('waiting...')
external_client.loop_forever()