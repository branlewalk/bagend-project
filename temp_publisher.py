from time import sleep
import json
from thermo import read_sensor
import pika
from datetime import datetime

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/'))
channel = connection.channel()
channel.exchange_declare(exchange='temps', exchange_type='fanout')


def publish(temp):
    channel.basic_publish(exchange='temps', routing_key='', body=json.dumps(temp),
                          properties=pika.BasicProperties(headers={'type': 'data'}))

now = datetime.now()
c_time = now.strftime("%H:%M:%S")

while True:
    all_temps = read_sensor()
    hlt = all_temps[0][1]
    mlt = all_temps[1][1]
    bk = all_temps[2][1]
    val = (hlt, mlt, bk)
    print("Values are: {} at {}".format(json.dumps(val), c_time))
    publish(val)
    print("Sent to Rabbit")
    sleep(1)

