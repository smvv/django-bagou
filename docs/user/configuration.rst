.. _install:

Configuration
=============

Server
------

Incoming messages
~~~~~~~~~~~~~~~~~

Its very easy to handle incoming messages with _Bagou_. First thing to do is to create
``events.py`` in you application folder.

::

    from bagou.utils import broadcast
    from bagou.events import on_close
    from bagou.events import on_message
    from bagou.events import on_subscribe


    @on_message(channel=r"^hello$")
    def welcome(client, channel, message):
        broadcast(
            event='message',
            channels=client.channels,
            data={'text': 'Hello world from server.')


    @on_subscribe(channel=r"^hello$")
    def broadcast_new_user(client, channel, message):
        broadcast(
            event='message',
            channels=client.channels,
            data={'text': 'Welcome on my channel.'})


    @on_close
    def broadcast_left_user(client):
        broadcast(
            event='message',
            channels=client.channels,
            data={'text': 'Goodbye from every channel.'})

You can ``broadcast`` has many message has you want in an event. It's also possible to
just anwser to the current socket like that:

::

    client.jsonify(event='message', data={'text': 'Hey, you websocket!'})


Client
------


