# -*- coding: utf-8 -*-
from bagou.events import on_close
from bagou.events import on_message
from bagou.events import on_subscribe
from bagou.utils import broadcast


@on_message(channel=r".*")
def broadcaster(client, channel, message, callback):
    broadcast(
        event='message',
        channel=client.channels,
        callback=callback,
        data={'name': client.store.get('username', 'Unknown'), 'text': message['data']})


@on_subscribe(channel=r".*")
def broadcast_new_user(client, channel, message, callback):
    broadcast(
        event='message',
        channel=client.channels,
        callback=callback,
        data={
            'name': 'System',
            'text': '%s user join chat room.' % client.store.get('username', 'Unknown')})


@on_close
def broadcast_left_user(client, channel, message, callback):
    broadcast(
        event='message',
        channel=client.channels,
        callback=callback,
        data={
            'name': 'System',
            'text': '%s user left chat room.' % client.store.get('username', 'Unknown')})


@on_subscribe(channel=r".*[dick|boobs|ass].*")
def vulgare_channel(client, channel, message, callback):
    client.jsonify(
        event='message',
        channel="dick", data={
            'name': 'BotMaster',
            'text': 'You chat room is dirty, if u know what i mean.'})
