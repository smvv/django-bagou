# -*- coding: utf-8 -*-
__version__ = "0.0.1"

import logging
from urlparse import urlparse
from django.utils.importlib import import_module
from django.conf import settings as django_settings

logging.basicConfig()
logger = logging.getLogger('bagou.general')
logger.setLevel(logging.INFO)

if not hasattr(django_settings, 'BAGOU'):
    settings = {}
    setattr(django_settings, 'BAGOU', settings)
else:
    settings = django_settings.BAGOU


settings.setdefault('AMQP_BROKER_URL', 'amqp://guest:guest@localhost:5672/')
settings.setdefault('WEBSOCKET_URL', 'ws://localhost:9000/websocket')
settings.setdefault('QUEUE_NAME', 'websocket')

__websocket_url = urlparse(settings.get('WEBSOCKET_URL'))
settings['WEBSOCKET_ADDR'] = __websocket_url.hostname
settings['WEBSOCKET_PORT'] = int(__websocket_url.port)
settings['WEBSOCKET_PATH'] = __websocket_url.path

__amqp_url = urlparse(settings.get('AMQP_BROKER_URL'))
settings['AMQP_BROKER_USER'] = __amqp_url.username
settings['AMQP_BROKER_PASS'] = __amqp_url.password
settings['AMQP_BROKER_ADDR'] = __amqp_url.hostname
settings['AMQP_BROKER_PORT'] = int(__amqp_url.port)
settings['AMQP_BROKER_PATH'] = __amqp_url.path


# Try and import an ``events`` module in each installed app,
# to ensure all event handlers are connected.
for app in django_settings.INSTALLED_APPS:
    try:
        import_module("%s.events" % app)
    except ImportError as err:
        logger.info('No events found in %s (%s)' % (app, err))
        pass
