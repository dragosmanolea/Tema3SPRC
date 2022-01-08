import paho.mqtt.client as mqtt
from typing import NewType
from time import sleep
from re import match
from datetime import date, datetime
import json

brokerMQTT = "localhost"

def on_message(client, user_data, msg):
    if not match(r'^[^/]+/[^/]+$', msg.topic):
        return
    topic = msg.topic

    topic_splitted = topic.split("/")
    location = topic_splitted[0]
    station = topic_splitted[1]

    timestamp = datetime.now()

    decodeMessage = msg.payload.decode("utf-8")
    current_payload = json.loads(decodeMessage)
    
    for it in current_payload:
        key = it
        value = current_payload.get(key, None)
        

def main():
    mqtt_cl = mqtt.Client(userdata="zoinx")
    mqtt_cl.on_message = on_message

    mqtt_cl.connect(brokerMQTT)
    mqtt_cl.subscribe('#')
    mqtt_cl.loop_forever()


if __name__ == "__main__":
    main()

# Dragos Manolea 343C5