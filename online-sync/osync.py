# -*- coding: utf8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
from enum import Enum, unique  # Requires Python 3.4
from warnings import warn
from zmq import LINGER, PUSH, PULL, Context


@unique
class Endpoints(Enum):
    source = 1
    sink = 2


class OSync:
    '''Watch for changes in a filesystem and send changed files via ZeroMQ
    to a secondary location.

    Changes in the filesystem are detected by INotify events. Implementation
    note: INotify is available for both Windows and Linux but the Python
    wrappers are limited to Linux >2.6.

    The timestamp of the first file event that was queued is kept as a lock
    file. This enables usage of tools like find to commit unchanged files to
    the transfer queue.

    The file transfer queue is a ZeroMQ one-on-one PUSH-PULL channel (but
    could also be PUB-SUB but not PAIR). The choice assumes that it is better
    to fail early if either side goes away (PUSH) than to silently lose
    messages (PUB) and later trace what has been lost. PAIR is considered
    experimental and for use with in-process queues only.

    Node coordination and intermediate state synchronisation uses a ZeroMQ
    REQ-REP channel similar to http://zguide.zeromq.org/page:all#toc47.

    The zmq channels neither provide encryption nor authentication. Therefore
    both endpoints are set to localhost and should be tunnelled through SSH-
    forwarded ports.
    '''
    def __init__(self, endpoint, port=None):
        '''Read service parameter and wait for start() to initiate the process.

        >>> OSync(endpoint=Endpoints.source, port=None)
        >>> OSync(endpoint=Endpoints.sink, port=49151)
        '''
        assert endpoint in Endpoints,\
            'endpoint must be member of Endpoints enumeration'
        self.endpoint = endpoint

        assert port is None or isinstance(port, int),\
            'Port must be None or an integer'
        if port is not None and (port < 1024 or port > 49151):
            warn(
                ('Not recommended port range. Avoid well-known and ephemeral '
                 'ports. Choose a port from [1024, 49151].'),
                RuntimeWarning
            )
        self.port = port

        # bind all nodes to ports on localhost
        self.common_ip_address = '127.0.0.1'

    def start(self):
        port = self.port
        context = Context()
        with context.socket(PUSH) as socket:
            socket.setsockopt(LINGER, 0)
            if port:
                socket.bind('tcp://{}:{}'.format(
                    self.common_ip_address,
                    port
                ))
            else:
                port = socket.bind_to_random_port(
                    'tcp://{}'.format(self.common_ip_address),
                    1024,   # min port
                    49152,  # max+1 port
                    10,     # max tries
                )

            print('Bound to port {}.'.format(port))
        context.term()
