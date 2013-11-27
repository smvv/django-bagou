# -*- coding: utf-8 -*-
from bagou.events import on_message
from bagou.utils.message import broadcast
from bagou.utils.message import broadcast_to_channel


@on_message(channel=r"room")
def broadcaster(client, message):
    broadcast(type='message', data={'name': 'Jean', 'text': message['data']})


@on_message(channel=r".*")
def channel_broadcaster(client, message):
    broadcast_to_channel(
        type='message', channel='room', data={'name': 'Miki', 'text': 'Im here'})
