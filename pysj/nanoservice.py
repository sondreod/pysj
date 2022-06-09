import logging
import os
import pickle
import select
import socket
import sys
from pathlib import Path
from time import sleep
from typing import Any, Callable, Iterable, Tuple

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class NanoServiceClient:
    """Simple client for consuming python software from multiple threads/processes"""

    def __init__(self, socket_filepath="nanoservice"):
        self.socket_filepath = str(
            Path(f"~/.{socket_filepath}.sock").expanduser().absolute()
        )

    def __getattr__(self, name):
        if name not in self.__dict__:

            def gen(*args, **kwargs):
                return self.__query(name, args, kwargs)

            return gen
        return super().__getattr__(name)

    def __query(self, name, args, kwargs):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        log.debug("connecting to {}".format(self.socket_filepath))
        try:
            sock.connect(self.socket_filepath)
        except socket.error as error:
            log.error(error)
            raise socket.error(error)

        try:

            data = pickle.dumps((name, args, kwargs))
            sock.sendall(str(len(data)).zfill(10).encode("utf-8") + data)
            packet_length = int(sock.recv(10))
            data = sock.recv(packet_length)
            return pickle.loads(data)

        finally:
            log.debug("closing socket")
            sock.close()


class NanoService:
    """Simple server for exposing python software"""

    def __init__(self, socket_filepath="nanoservice"):
        self.socket_filepath = str(
            Path(f"~/.{socket_filepath}.sock").expanduser().absolute()
        )

    functions = dict()

    def start(self):
        log.debug("Starting server")
        for f in self.functions:
            log.debug(f"Registered f: {f}")

        try:
            os.unlink(self.socket_filepath)
        except OSError:
            if os.path.exists(self.socket_filepath):
                raise

        log.debug("starting up on {}".format(self.socket_filepath))

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(self.socket_filepath)
        sock.listen()

        try:
            while True:
                log.debug("waiting for a connection")
                connection, client_address = sock.accept()
                try:
                    log.debug("connection received")
                    packet_length = int(connection.recv(10))
                    data = connection.recv(packet_length)

                    function, args, kwargs = pickle.loads(data)
                    func = self.functions.get(function)
                    output = func(*args, **kwargs)
                    data = pickle.dumps(output)
                    connection.sendall(str(len(data)).zfill(10).encode("utf-8") + data)

                finally:
                    connection.close()
        finally:
            try:
                os.unlink(self.socket_filepath)
            except OSError:
                pass

    def endpoint(self):
        """Register a function to expose through the service"""

        def wrap(func):
            self.functions[func.__name__] = func
            return func

        return wrap


if __name__ == "__main__":

    service = NanoService()

    @service.endpoint()
    def double(s):
        return s * 2

    service.start()
