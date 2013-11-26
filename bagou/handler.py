# -*- coding: utf-8 -*-
import json
import logging
import tornado.websocket

from .events import on_message

logging.basicConfig()
logger = logging.getLogger("Handler")
logger.setLevel(logging.INFO)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        self.channels = []
        self.authenticated = False
        self.user = None

        self.application.pika_client.add_event_listener(self)
        logger.info("WebSocket opened")

    def on_close(self):
        logger.info("WebSocket closed")
        self.application.pika_client.remove_event_listener(self)

    def on_message(self, message):
        logger.info("Message received: %s " % message)
        message_json = json.loads(message)
        if message_json.get('type') == 'subscribe':
            channel = message_json.get('data', {}).get('channel')
            if channel:
                logger.info("Subscribing to %s channel." % channel)
                self.channels.append(channel)
                self.jsonify(
                    type="subscribe", data={'channel': channel, 'status': True})
        elif message_json.get('type') == 'unsubscribe':
            channel = message_json.get('data', {}).get('channel')
            if channel:
                logger.info("Unsubscribing to %s channel." % channel)
                self.channels.remove(channel)
                self.jsonify(
                    type="unsubscribe", data={'channel': channel, 'status': True})
        else:
            on_message.send(self, message_json)

    def jsonify(self, **kwargs):
        self.write_message(kwargs)
