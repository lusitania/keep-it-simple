# -*- coding: utf8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
'''One-off handshake using command protocol.

The module supports command line invocation (load service first):
    TerminalA> python3 -m zmq-one-off-handshake --serve
    TerminalB> python3 -m zmq-one-off-handshake --register

See zmq-simplex.py for extend documentation of PyZMQ calls.
'''

import zmq


class Handshake:
    '''Rudimentary handshake implementation (ordered message exchange).

    Beware that reliability considerations are not done here.
    See http://zguide.zeromq.org/page:all#toc86

    ØMQ essentials:
        Responding:
            zmq.Context().socket(REP)
            socket.bind()
            socket.send_pyobj()
        Requesting:
            zmq.Context().socket(REQ)
            socket.connect()
            socket.recv_pyobj()
    '''

    def __init__(self):
        '''Define service address.'''
        self.address = 'tcp://127.0.0.1:5555'

    def respond(self):
        '''Create and open sending endpoint of channel. Also read text from
        STDIN and publish it to the channel.

        Beware that subscribe() and publish() are mutually exclusive, here.
        '''
        context = zmq.Context()
        sock = context.socket(zmq.REP)
        sock.bind(self.address)

        print("Service started")

        request = sock.recv_pyobj()
        assert 'command' == request['topic']
        assert 'register' == request['payload']

        print('Registration received')

        sock.send_pyobj({'topic': 'command', 'payload': 'terminate'})

        print('Line termination sent. Exiting.')

        sock.close(linger=0)
        context.term()

    def request(self):
        '''Create and open receiving endpoint of channel. Also subscribe to
        messages from the channel and write then to STDOUT.

        Beware that subscribe() and publish() are mutually exclusive, here.
        '''
        context = zmq.Context()
        sock = context.socket(zmq.REQ)
        sock.connect(self.address)

        sock.send_pyobj({'topic': 'command', 'payload': 'register'})

        print('Registration sent')

        response = sock.recv_pyobj()
        assert 'command' == response['topic']
        assert 'terminate' == response['payload']

        print('Termination received. Exiting.')

        sock.close(linger=0)
        context.term()


# Some trivial CLI
if __name__ == '__main__':
    from argparse import ArgumentParser

    p = ArgumentParser(
        description='do a one-off message handshake using 0mq'
    )

    modes = p.add_mutually_exclusive_group(required=True)
    modes.add_argument(
        '-s', '--serve',
        action='store_true',
        help='assume server position in channel',
    )
    modes.add_argument(
        '-r', '--register',
        action='store_true',
        help='register with service',
    )

    channel = Handshake()

    args = p.parse_args()
    if args.serve:
        channel.respond()
    elif args.register:
        channel.request()
