from json import dumps, load
from numpy import arange
from random import choice
from sys import stdin
from time import sleep

import paho.mqtt.client as mqtt


def _create_connection():
    client = mqtt.Client("dragos e34")
    client.connect("localhost")
    client.loop_start()

    return client


client = _create_connection()

batts = list(range(50, 150))
temps = list(range(10, 300))
humids = list(range(5, 95))
secs = list(arange(1, 1.5, 2))
stations = ['A', 'B', 'C']

while True:
    iot_data = {
        'BAT': choice(batts),
        'TEMP': choice(temps),
        'HUMID': choice(humids),
    }

    station = choice(stations)
    print(station)

    client.publish('UPB/' + station, dumps(iot_data))
    
    print(f'Station {station} published:\n{dumps(iot_data, indent=4)}\n')
    sleep(choice(secs))
