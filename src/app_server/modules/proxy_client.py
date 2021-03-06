import logging
import socket
import time

from modules.protocol import net
from modules.protocol import types


class ProxyClientError(Exception):
    def __init__(self, *args, **kwargs):
        super(ProxyClientError, self).__init__(*args, **kwargs)


class ProxyClient(object):
    '''A proxy to the server.

    Attributes:
        _sock: The socket object.
        _logger: The logger.
    '''
    def __init__(self, addr, port, logger):
        '''Constructor.

        Args:
            addr: Address of the server.
            port: Port of the server.
            logger: The logger.
        '''
        self._addr = addr
        self._port = port
        self._logger = logger

        self._sock = None

        self._init_sock()

    def send_pkg(self, typee, buf):
        '''Send a buf with specifying package type.

        Args:
            typee: The package type.
            buf: The package content.
        '''
        for i in range(10):
            try:
                self._sock.sendall(
                        net.PackageHeader(typee, len(buf)).dump() + buf)
                return
            except socket.error as e:
                self._logger.warning('It seems that the server is dead.')
                try:
                    self._sock.close()
                except Exception as _:
                    pass
                time.sleep(10)
                self._init_sock()
        raise ProxyClientError('Cannot send message.')

    def recv_header(self):
        '''Receives a package header.

        Returns: An instance of `net.PackageHeader`
        '''
        buf = self.recv_all(net.PackageHeader.SIZE)
        return net.PackageHeader.load(buf)[0]

    def recv_all(self, sz):
        '''Receives all bytes from the server.

        Args:
            sz: Number of bytes to receive.

        Returns: An array of bytes.
        '''
        buf = b''
        while len(buf) < sz:
            try:
                a = self._sock.recv(sz - len(buf))
            except socket.error as e:
                raise ProxyClientError('Cannot recv: %r' % e)
            if not a:
                raise ProxyClientError('Cannot recv.')
            buf += a
        return buf

    def _init_sock(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._addr, self._port))
            self._logger.info('Connected to the server (%s, %d)'
                              % (self._addr, self._port))
        except socket.error as e:
            raise ProxyClientError('Cannot connect to the miner server %r' % e)
