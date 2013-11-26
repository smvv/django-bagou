# -*- coding: utf-8 -*-
import json
import pika

from django.conf import settings


def __send(message):
    cred = pika.PlainCredentials(
        settings.BAGOU.get('AMQP_BROKER_USER'),
        settings.BAGOU.get('AMQP_BROKER_PASS'))

    param = pika.ConnectionParameters(
        host=settings.BAGOU.get('AMQP_BROKER_ADDR'),
        port=settings.BAGOU.get('AMQP_BROKER_PORT'),
        virtual_host=settings.BAGOU.get('AMQP_BROKER_PATH'),
        credentials=cred)

    body = json.dumps(message)

    conn = pika.BlockingConnection(param)
    channel = conn.channel()
    channel.basic_publish(
        exchange='', routing_key=settings.BAGOU.get('QUEUE_NAME'), body=body)


def broadcast(**kwargs):
    __send(kwargs)


def broadcast_to_channel(channel, **kwargs):
    kwargs['channel'] = channel
    __send(kwargs)
