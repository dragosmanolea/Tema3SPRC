import paho.mqtt.client as mqtt
from typing import NewType
from time import sleep

brokerMQTT = "localhost"

def on_message(client, user_data, msg):
    topic = msg.topic
    decodeMessage = str(msg.payload.decode("utf-8"))
    print("Topic: " + topic)
    print("Message: " + decodeMessage)

def main():
    mqtt_cl = mqtt.Client(userdata="zoinx")
    mqtt_cl.on_message = on_message

    mqtt_cl.connect(brokerMQTT)
    mqtt_cl.subscribe('#')
    mqtt_cl.loop_forever()


if __name__ == "__main__":
    main()

# Dragos Manolea 343C5