# -*- coding: utf-8 -*-
import json
import logging
import tornado.websocket

from .events import on_open
from .events import on_close
from .events import on_store
from .events import on_message
from .events import on_subscribe
from .events import on_unsubscribe

logging.basicConfig()
logger = logging.getLogger("tornado.handler")
logger.setLevel(logging.INFO)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        self.channels = []
        self.authenticated = False
        self.user = None

        self.store = {}

        self.application.pika_client.add_event_listener(self)
        on_open.send(self)
        logger.info("WebSocket opened")

    def on_close(self):
        logger.info("WebSocket closed")
        self.application.pika_client.remove_event_listener(self)
        on_close.send(self)

    def _on_subscribe(self, message):
        channel = message.get('data', {}).get('channel')
        callback_id = message.get('callbackId')
        if channel:
            logger.info("Subscribing to '%s' channel." % channel)
            self.channels.append(channel)
            on_subscribe.send(self, message, channel, callback_id)

    def _on_unsubscribe(self, message):
        channel = message.get('data', {}).get('channel')
        callback_id = message.get('callbackId')
        if channel:
            logger.info("Unsubscribing to '%s' channel." % channel)
            self.channels.remove(channel)
            on_unsubscribe.send(self, message, channel, callback_id)

    def _on_store(self, message):
        callback_id = message.get('callbackId')
        self.store.update(message.get('data'))
        on_store.send(self, message, callback_id)

    def on_message(self, message):
        logger.info("Message received: %s " % message)

        message_json = json.loads(message)
        if not isinstance(message_json, dict):
            self.jsonify(event="error", data={'message': 'bad message format'})

        message_event = message_json.get('event')
        if message_event == 'subscribe':
            self._on_subscribe(message_json)
        elif message_event == 'unsubscribe':
            self._on_unsubscribe(message_json)
        elif message_event == 'store':
            self._on_store(message_json)
        else:
            logger.info('Calling on_message event handlers')
            on_message.send(self, message_json)

    def jsonify(self, **kwargs):
        self.write_message(kwargs)
