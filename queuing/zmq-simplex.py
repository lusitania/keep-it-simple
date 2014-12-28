# -*- coding: utf8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
'''Hands-on simplex chat implementation.

The module supports command line invocation (any order of invocation):
    TerminalA> python3 -m zmq-simplex -s
    TerminalB> python3 -m zmq-simplex -p

    (TerminalB)> go type stuff
    (TerminalA){'id': datetime.datetime(...), 'message': 'go type stuff'}
'''

import zmq


class Simplexer:
    '''Rudimentary simplex publisher-subscriber implementation (unsolicited
    message exchange).

    This is a simple, one-directional chat application without indicators
    for publisher initiated line termination. See zmq-one-off-handshake.py
    for details.

    ØMQ essentials:
        Publishing:
            zmq.Context().socket(PUB)
            socket.bind()
            socket.send_pyobj()
        Subscription:
            zmq.Context().socket(SUB)
            socket.connect()
            socket.recv_pyobj()
    '''

    def __init__(self):
        '''Initialise ØMQ context and define socket options for publishing and
        subscription.
        '''

        # The zmq_connect() function connects the socket to an endpoint and
        # then accepts incoming connections on that endpoint.
        #
        # https://zeromq.github.io/pyzmq/api/zmq.html#zmq.Context
        # http://api.zeromq.org/4-0:zmq-connect
        self.context = zmq.Context()

        # The endpoint is a string consisting of a transport :// followed by
        # an address. The transport specifies the underlying protocol to use.
        # The address specifies the transport-specific address to connect to.
        # ØMQ provides the the following transports:
        #   http://api.zeromq.org/4-0:zmq_tcp
        #   http://api.zeromq.org/4-0:zmq_ipc       (local inter-process)
        #   http://api.zeromq.org/4-0:zmq_inproc    (local in-process)
        #   http://api.zeromq.org/4-0:zmq_pgm       (multicast)
        self.address = 'tcp://127.0.0.1:5555'

        # A socket of type ZMQ_SUB is used by a subscriber to subscribe to
        # data distributed by a publisher. Initially a ZMQ_SUB socket is not
        # subscribed to any messages, use the ZMQ_SUBSCRIBE option of
        # zmq_setsockopt(3) to specify which messages to subscribe to. The
        # zmq_send() function is not implemented for this socket type.
        #
        # http://api.zeromq.org/4-0:zmq-socket#toc10
        self.subscribe_sock = zmq.SUB
        self.publish_sock = zmq.PUB

        # The ZMQ_SUBSCRIBE option shall establish a new message filter on a
        # ZMQ_SUB socket. Newly created ZMQ_SUB sockets shall filter out all
        # incoming messages, therefore you should call this option to establish
        # an initial message filter.
        #
        # An empty option_value of length zero shall subscribe to all incoming
        # messages. A non-empty option_value shall subscribe to all messages
        # beginning with the specified prefix. Multiple filters may be
        # attached to a single ZMQ_SUB socket, in which case a message shall
        # be accepted if it matches at least one filter.
        #
        # See http://api.zeromq.org/4-0:zmq-setsockopt#toc6
        self.subscribe_allmsg = (zmq.SUBSCRIBE, b'')

        # Register a simple termination signal
        # Note: Signalling in general is a tricky thing so don't expect much
        # at this point.
        def terminate(signal, frame):
            '''Signal callback to terminate the program.'''

            print("Terminating")
            import sys
            self.__del__()
            sys.exit()  # Apparently this is the only way to abort input()

        from signal import signal, SIGINT
        signal(SIGINT, terminate)

    def __del__(self):
        '''Close all open resources on object disposal.'''
        if self.context.closed:
            return

        self.sock.close()
        self.context.term()

    def publish(self):
        '''Create and open sending endpoint of channel. Also read text from
        STDIN and publish it to the channel.

        Beware that subscribe() and publish() are mutually exclusive, here.
        '''

        # https://zeromq.github.io/pyzmq/api/zmq.html#zmq.Context.socket
        self.sock = self.context.socket(self.publish_sock)

        # https://zeromq.github.io/pyzmq/api/zmq.html#zmq.Socket.bind
        self.sock.bind(self.address)

        print("Publishing on {}. Ctrl-C to abort.".format(self.address))

        from datetime import datetime

        while True:
            text = input("> ")

            # Note: Common Python data structures have build-in support
            msg = {"topic": "chat", "id": datetime.now(), "message": text}

            # https://zeromq.github.io/pyzmq/api/zmq.html#zmq.Socket.send_pyobj
            # Send Flags: http://api.zeromq.org/4-0:zmq-send#toc2
            self.sock.send_pyobj(msg)

    def subscribe(self):
        '''Create and open receiving endpoint of channel. Also subscribe to
        messages from the channel and write then to STDOUT.

        Beware that subscribe() and publish() are mutually exclusive, here.
        '''

        # https://zeromq.github.io/pyzmq/api/zmq.html#zmq.Context.socket
        self.sock = self.context.socket(self.subscribe_sock)

        # https://zeromq.github.io/pyzmq/api/zmq.html#zmq.Socket.setsockopt
        self.sock.setsockopt(*self.subscribe_allmsg)

        # https://zeromq.github.io/pyzmq/api/zmq.html#zmq.Socket.connect
        self.sock.connect(self.address)

        print("Subscribing to {}. Ctrl-C to abort.".format(self.address))

        while True:
            # https://zeromq.github.io/pyzmq/api/zmq.html#zmq.Socket.recv_pyobj
            # Receive Flags: http://api.zeromq.org/4-0:zmq-recv#toc2
            msg = self.sock.recv_pyobj()

            print(msg)


# Some trivial CLI
if __name__ == '__main__':
    from argparse import ArgumentParser

    p = ArgumentParser(
        description='send a message through a simplex channel using 0mq'
    )

    modes = p.add_mutually_exclusive_group(required=True)
    modes.add_argument(
        '-p', '--publish',
        action='store_true',
        help='assume publisher position in simplex channel',
    )
    modes.add_argument(
        '-s', '--subscribe',
        action='store_true',
        help='assume subscriber position in simplex channel',
    )

    channel = Simplexer()

    args = p.parse_args()
    if args.publish:
        channel.publish()
    elif args.subscribe:
        channel.subscribe()
