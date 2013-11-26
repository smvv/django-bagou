# -*- coding: utf-8 -*-
import os
import json
import logging
import tornado.web
import tornado.ioloop
import tornado.template
import tornado.websocket

from django.conf import settings
from django.template import loader
from django.template import Context

from .client import PikaClient
from .events import on_message


logging.basicConfig()
logger = logging.getLogger("Tornado")
logger.setLevel(logging.INFO)

RESOURCES_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        t = loader.get_template('index.html')
        c = Context({})
        self.write(t.render(c))


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        self.application.pika_client.add_event_listener(self)
        logger.info("WebSocket opened")

    def on_close(self):
        logger.info("WebSocket closed")
        self.application.pika_client.remove_event_listener(self)

    def on_message(self, message):
        logger.info("Message received: %s " % message)
        message_json = json.loads(message)
        on_message.send(self, message_json)


class WebSocketServer(object):
    def __init__(self):
        self.io_loop = tornado.ioloop.IOLoop.instance()
        self.pika_client = PikaClient(self.io_loop)

        self.application = tornado.web.Application()
        self.application.pika_client = self.pika_client

        self.hostname = "%s:%s" % (
            settings.BAGOU.get('WEBSOCKET_ADDR'), settings.BAGOU.get('WEBSOCKET_PORT'))

    def _add_default_handlers(self):
        self.application.add_handlers(r'.*', [
            (r"/", MainHandler),
            (r"%s" % settings.BAGOU.get('WEBSOCKET_PATH'), WebSocketHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {"path": RESOURCES_ROOT})])

    def run(self):
        self._add_default_handlers()

        self.application.pika_client.connect()
        self.application.listen(int(settings.BAGOU.get('WEBSOCKET_PORT')))
        self.io_loop.start()

    def stop(self):
        for websocket in self.pika_client.event_listeners:
            websocket.close()
        self.io_loop.stop()
