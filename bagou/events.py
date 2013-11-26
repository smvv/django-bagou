# -*- coding: utf-8 -*-
import re


class EventError(Exception):
    pass


class Event(object):
    """
    Signal-like object for Websocket events that supports
    filtering on channels. Registering event handlers is
    performed by using the Event instance as a decorator::

    @on_message
    def message(handler, message):
    ...

    Event handlers can also be registered for particular
    channels using the channel keyword argument with a
    regular expression pattern::

    @on_message(channel="^room-")
    def message(handler, message):
    ...

    The ``on_connect`` event cannot be registered with a
    channel pattern since channel subscription occurs
    after a connection is established.
    """

    def __init__(self, supports_channels=True):
        self.supports_channels = supports_channels
        self.handlers = []

    def __call__(self, handler=None, channel=None):
        """
        Decorates the given handler. The event may be called
        with only a channel argument, in which case return a
        decorator with the channel argument bound.
        """
        if handler is None:
            def handler_with_channel(handler):
                return self.__call__(handler, channel)
            return handler_with_channel
        if channel:
            if not self.supports_channels:
                raise EventError("The %s event does not support channels so "
                                 "the handler `%s` could not be registered" %
                                 self.name, handler.__name__)
            channel = re.compile(channel)
        self.handlers.append((handler, channel))

    def send(self, client, message, *args):
        """
        When an event is sent, run all relevant handlers. Relevant
        handlers are those without a channel pattern when the given
        socket is not subscribed to any particular channel, or the
        handlers with a channel pattern that matches any of the
        channels that the given socket is subscribed to.

        In the case of subscribe/unsubscribe, match the channel arg
        being sent to the channel pattern.
        """
        for handler, pattern in self.handlers:
            no_channel = not pattern and not client.channels
            if self.name.endswith("subscribe") and pattern:
                matches = [pattern.match(args[0])]
            else:
                matches = [pattern.match(c) for c in client.channels if pattern]
            if no_channel or filter(None, matches):
                handler(handler, message, *args)

on_message = Event()
on_subscribe = Event()
on_unsubscribe = Event()

# Give each event a name attribute.
for k, v in globals().items():
    if isinstance(v, Event):
        setattr(v, "name", k)
