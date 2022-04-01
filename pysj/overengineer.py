import json
import logging
import socketserver
from curses.ascii import EM
from datetime import datetime, timedelta
from multiprocessing import Process, Queue
from pathlib import Path
from queue import Empty
from time import sleep, time
from urllib.parse import parse_qs, urlsplit

from numpy import true_divide

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class WebhookTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(2048).strip()

        url = data.decode("utf-8").split(" HTTP/")[0][4:].strip()  # Get url of request
        resource, queryparams = urlsplit(url).path[1:], parse_qs(urlsplit(url).query)

        self.server.accepted_webhooks.put((resource, queryparams))
        log.debug("Webhook received")
        self.request.sendall(
            b"HTTP/1.1 201 ACCEPTED\r\nCache-Controll: no-cache\r\nConnection: close\r\n\r\n"
        )


class WebhookTCPServer(socketserver.TCPServer):
    def __init__(self, server_address, request_handler, accepted_webhooks):
        socketserver.TCPServer.__init__(self, server_address, request_handler)
        self.accepted_webhooks = accepted_webhooks
        self.allow_reuse_address = True
        self.server_activate()


def webhook_server(accepted_webhooks):
    """Minimal webserver accepting webhooks"""
    with WebhookTCPServer(
        ("0.0.0.0", 4488), WebhookTCPHandler, accepted_webhooks
    ) as server:
        server.allow_reuse_address = True
        server.server_activate()
        server.serve_forever()


class SchedulableProcess:
    def __init__(self, target=None, args=None, name=None, **kwargs):

        self.target = target
        self.args = args if args else ()
        self.triggers = kwargs
        self.name = name if name else target.__name__
        self.proc = None
        self.last_run = None

    def start(self, args=None):
        args = args if args else self.args
        log.info(f"Running process {self.name}")
        self.proc = Process(target=self.target, args=args, name=self.name)
        self.last_run = datetime.now()
        self.proc.start()

    def tick(self):
        if not self.proc or not self.proc.is_alive():
            if not self.triggers:
                self.start()
                return
            for trigger, value in self.triggers.items():
                if trigger == "after":
                    if self.last_run is None:
                        if datetime.fromisoformat(value) < datetime.now():
                            self.start()
                    elif trigger == "interval":
                        if (
                            self.last_run is None
                            or self.last_run + timedelta(seconds=value) < datetime.now()
                        ):
                            self.start()
                    elif trigger == "webhook":
                        pass  # Webhook triggers are handled in the event loop
                    else:
                        log.info(f"Unknown trigger ignored. ({trigger}).")

    def write_last_run_to_file(self):
        """TODO: Create save config func (e.g. last_run)"""
        config = json.load(Path("~/.overengineer").expanduser())
        if config_update := config.get(self.name):
            self.args = self.args + config_update


class OverEngineer:
    """
    TODO:
    - systemd service script that makes file paths to file/console
    - script entrypoint to script creating systemd unitfile
    """

    def __init__(self):
        self.accepted_webhooks = Queue()

        self.procs = [
            SchedulableProcess(target=webhook_server, args=(self.accepted_webhooks,))
        ]

    def register(self, *schedulable_processes):
        self.procs.extend(schedulable_processes)

    def start_event_loop(self):
        try:
            while True:  # Event loop
                for process in self.procs:
                    process.tick()

                if not self.accepted_webhooks.empty():  # There are cookies
                    try:
                        resource, args = self.accepted_webhooks.get_nowait()
                        for process in self.procs:
                            if process.name == resource:
                                log.info(
                                    f"Processing webhook (1/{self.accepted_webhooks.qsize()+1}, {resource}, {args}"
                                )
                                process.start(args=args.get("arg"))
                                break

                    except Empty:
                        pass  # They lied
                sleep(1)
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        for process in [x.proc for x in self.procs]:
            if (
                process and process.is_alive()
            ):  # Running is_alive has a side effect of joining proc if finished
                process.terminate()
                process.join(1)
                if process and process.is_alive():
                    process.kill()
                    process.join(1)
