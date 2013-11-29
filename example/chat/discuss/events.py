# -*- coding: utf-8 -*-
from bagou.utils import broadcast
from bagou.events import on_close
from bagou.events import on_message
from bagou.events import on_subscribe


@on_message(channel=r".*")
def broadcaster(client, channel, message, callback):
    broadcast(
        event='message',
        channels=client.channels,
        callback=callback,
        data={
            'name': client.store.get('username', 'Unknown'),
            'text': message.get('data', {}).get('content')})


@on_subscribe(channel=r".*")
def broadcast_new_user(client, channel, message, callback):
    broadcast(
        event='message',
        channels=client.channels,
        callback=callback,
        data={
            'name': 'System',
            'text': '%s join chat room.' % client.store.get('username', 'Unknown')})


@on_close
def broadcast_left_user(client):
    broadcast(
        event='message',
        channels=client.channels,
        data={
            'name': 'System',
            'text': '%s left chat room.' % client.store.get('username', 'Unknown')})


@on_subscribe(channel=r"dick|boobs|ass")
def vulgare_channel(client, channel, message, callback):
    client.jsonify(
        event='message',
        channels="dick",
        data={'name': 'System', 'text': 'You chat room is dirty, if u know what i mean.'})
