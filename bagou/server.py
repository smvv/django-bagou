# -*- coding: utf-8 -*-
import logging
import tornado.web
import tornado.ioloop
import tornado.template

from django.conf import settings

from .client import PikaClient
from .handler import WebSocketHandler

logging.basicConfig()
logger = logging.getLogger("tornado.general")
logger.setLevel(logging.INFO)


class WebSocketServer(object):
    def __init__(self):
        self.io_loop = tornado.ioloop.IOLoop.instance()
        self.pika_client = PikaClient(self.io_loop)

        self.application = tornado.web.Application()
        self.application.add_handlers(r'.*', [
            (r"%s" % settings.BAGOU.get('WEBSOCKET_PATH'), WebSocketHandler)])
        self.application.pika_client = self.pika_client

        self.hostname = "%s:%s" % (
            settings.BAGOU.get('WEBSOCKET_ADDR'), settings.BAGOU.get('WEBSOCKET_PORT'))

    def run(self):
        logger.info('Listening on %s:%s...' % (
            settings.BAGOU.get('WEBSOCKET_ADDR'),
            settings.BAGOU.get('WEBSOCKET_PORT')))
        self.application.pika_client.connect()
        self.application.listen(int(settings.BAGOU.get('WEBSOCKET_PORT')))
        self.io_loop.start()

    def stop(self):
        for websocket in self.pika_client.event_listeners:
            websocket.close()
        self.io_loop.stop()
