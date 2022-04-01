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

socket_filepath = str(Path("~/.nanoservice.sock").expanduser().absolute())


class NanoServiceClient:
    """Simple client for consuming python software from multiple threads/processes"""

    def __getattr__(self, name):
        if name not in self.__dict__:

            def gen(*args, **kwargs):
                return self.__query(name, args, kwargs)

            return gen
        return super().__getattr__(name)

    def __query(self, name, args, kwargs):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_address = socket_filepath
        log.debug("connecting to {}".format(server_address))
        try:
            sock.connect(server_address)
        except socket.error as error:
            log.error(error)
            sys.exit(1)

        try:

            message = pickle.dumps((name, args, kwargs))
            sock.sendall(message)
            data = b""
            timeout = 10  # TODO: Implement a simple protocol with packet length so timeout can be removed
            while True:
                if incomming_data := self._recv_timeout(sock, 2048, timeout):
                    data += incomming_data
                    timeout = 0.01
                    log.debug("received {!r}".format(pickle.loads(data)))
                else:
                    break
            return data

        finally:
            log.debug("closing socket")
            sock.close()

    @staticmethod
    def _recv_timeout(sock, bytes_to_read, timeout_seconds):
        sock.setblocking(0)
        ready = select.select([sock], [], [], timeout_seconds)
        if ready[0]:
            return sock.recv(bytes_to_read)

        return None


class NanoService:
    """Simple server for exposing python software"""

    functions = dict()

    def start(self):
        log.debug("Starting server")
        for f in self.functions:
            log.debug(f"Registered f: {f}")

        server_address = socket_filepath

        try:
            os.unlink(server_address)
        except OSError:
            if os.path.exists(server_address):
                raise

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        log.debug("starting up on {}".format(server_address))
        sock.bind(server_address)

        sock.listen()

        while True:
            log.debug("waiting for a connection")
            connection, client_address = sock.accept()
            try:
                log.debug("connection from", client_address)

                while True:
                    data = connection.recv(2048)
                    if data:
                        function, args, kwargs = pickle.loads(data)
                        func = self.functions.get(function)
                        output = func(*args, **kwargs)
                        sleep(1)
                        connection.sendall(pickle.dumps(output))
                    else:
                        break

            finally:
                connection.close()

    def endpoint(self):
        """Register a function to expose through the service"""

        def wrap(func):
            self.functions[func.__name__] = func
            return func

        return wrap


if __name__ == "__main__":

    service = NanoService()

    @service.endpoint()
    def echo(s):
        return s * 4

    service.start()
