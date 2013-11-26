import json
import pika


def send(**kwargs):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    body = json.dumps(kwargs)
    channel.basic_publish(exchange='', routing_key='bagou', body=body)
