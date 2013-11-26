# -*- coding: utf-8 -*-
import logging
import tornado.web
import tornado.ioloop
import tornado.template

from django.conf import settings

from .client import PikaClient
from .handler import WebSocketHandler

logging.basicConfig()
logger = logging.getLogger("Tornado")
logger.setLevel(logging.INFO)


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
            (r"%s" % settings.BAGOU.get('WEBSOCKET_PATH'), WebSocketHandler)])

    def run(self):
        self._add_default_handlers()

        self.application.pika_client.connect()
        self.application.listen(int(settings.BAGOU.get('WEBSOCKET_PORT')))
        self.io_loop.start()

    def stop(self):
        for websocket in self.pika_client.event_listeners:
            websocket.close()
        self.io_loop.stop()
