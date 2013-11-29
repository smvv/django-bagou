.. _introduction:

Introduction
============

Bagou is a Tornado_ WebSocket server with a Pika_ client connected on RabbitMQ_ in a asynchronous
loop.
This architecture allow you to send websocket message to channel without having
incoming message.

Incoming
--------

Incoming messages are catched by Tornado and sent to method that you can decorate.
This is a simple workflow.


Sending
-------

Send a message is a little more complexe.
You can send message to websocket after an incoming message, easy.

But when you want to send message in a Celery_ task for example, or after an SQL update
statement, you'll have to use an easy method which do all the job.

This is it.

You can broadcast message when you want, which will internaly be publish on RabbitAMQ,
consumed by Pika client. Pika which run in the same loop as Tornado, sent message to connected websockets.

Client side
-----------

A ``BagouWebSocket`` javascript Object is provided which implement almost all SocketIO_
mechanisms which I recommend you to read.

Bagou License
-------------

    .. include:: ../../LICENSE


.. _Tornado: http://www.tornadoweb.org/en/stable/index.html
.. _Pika: http://pika.readthedocs.org/en/latest/
.. _RabbitMQ: http://www.rabbitmq.com/
.. _Celery: http://www.celeryproject.org/
.. _SocketIO: http://socket.io/
