import paho.mqtt.client as mqtt
from typing import NewType
from time import sleep, time
from re import match
from datetime import date, datetime
import json
import logging
from influxdb import InfluxDBClient

brokerMQTT = "mosquitto_mqtt_broker"

def on_message(client, user_data, msg):
    if not match(r'^[^/]+/[^/]+$', msg.topic):
        return
    topic = msg.topic

    logging.info(f'Received a message by topic [{topic}]')
    print(f'Received a message by topic [{topic}]')
    topic_splitted = topic.split("/")
    location = topic_splitted[0]
    station = topic_splitted[1]

    decodeMessage = msg.payload.decode("utf-8")
    current_payload = json.loads(decodeMessage)

    for it in current_payload:
        key = it
        value = current_payload.get(key, None)
        if key == "timestamp":
            timestamp = datetime.strptime(value, "%Y-%m-%d %H:%M:%S%z")
            logging.info(f"Data timestamp is: {timestamp}")
            print(f"Data timestamp is: {timestamp}")
        else:
            timestamp = datetime.now()
            logging.info(f"Data timestamp is NOW")
            print(f"Data timestamp is NOW")
        data = []
        if isinstance(value, int) or isinstance(value, float):
            # valid input
            data.append({
                "measurement": f"{station}.{key}",
                "tags": {
                    "location": location,
                    "station": station
                },
                "fields": {
                    "value": value
                },
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S%z")
            })

            logging.info(f"{location}.{station}.{key} {value}")
            print(f"{location}.{station}.{key} {value}")

            if data:
                # print(f"ar trebui sa adaug in DB: {data}")
                user_data.write_points(data)

def main():
    client_db = InfluxDBClient(host='influxdb', port=8086)
    databases = client_db.get_list_database()
    # check if db exists
    if len(list(filter(lambda x: x['name'] == "iot_db", databases))) == 0:
        client_db.create_database("iot_db")
    client_db.switch_database("iot_db")

    mqtt_cl = mqtt.Client(userdata=client_db)
    mqtt_cl.on_message = on_message

    mqtt_cl.connect(brokerMQTT)
    mqtt_cl.subscribe('#')
    mqtt_cl.loop_forever()


if __name__ == "__main__":
    main()

# Dragos Manolea 343C5