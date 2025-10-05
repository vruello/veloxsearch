from http import HTTPStatus
from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer,
    ThreadingHTTPServer,
)
import logging
import argparse
import json
from socketserver import BaseRequestHandler
from typing import Any, Callable, Self
import typing
import urllib.parse

from velox_search.velox import Velox

from ..config import Config


class VeloxHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Serve a GET request
        """
        try:
            url = urllib.parse.urlparse(self.path)
        except Exception as e:
            logging.warning(
                "Received invalid url from %s: %s. %s",
                self.client_address,
                self.path,
                e,
            )
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.flush_headers()
            return

        if url.path != "/autocomplete":
            self.send_response(HTTPStatus.NOT_FOUND)
            self.flush_headers()
            return

        try:
            query_params = urllib.parse.parse_qs(url.query)
        except Exception as e:
            logging.warning(
                "Received invalid query from %s: %s. %s",
                self.client_address,
                url.query,
                e,
            )
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.flush_headers()
            return

        query = query_params.get("query")
        if query is None or len(query) > 1:
            # Missing argument
            self.send_response(HTTPStatus.UNPROCESSABLE_CONTENT)
            self.flush_headers()
            return

        prefix = query[0]
        # self.server is typed as a ThredingHTTPServer, but it is a VeloxHTTPServer
        velox = typing.cast(VeloxHTTPServer, self.server).velox_instance
        logging.info("Compute word list for prefix %s", prefix)

        try:
            words = velox.complete_prefix(prefix)
        except Exception as e:
            logging.error("Failed to fetch words with prefix `%s`: %s", prefix, e)
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.flush_headers()
            return

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(words).encode())


class VeloxHTTPServer(ThreadingHTTPServer):
    """
    This subclass is used to inject <velox_instance> in HTTP server
    """

    def __init__(
        self,
        velox_instance: Velox,
        server_address: (
            tuple[str | bytes | bytearray, int]
            | tuple[str | bytes | bytearray, int, int, int]
        ),
        RequestHandlerClass: Callable[[Any, Any, Self], BaseRequestHandler],
        bind_and_activate: bool = True,
    ) -> None:
        self.velox_instance = velox_instance
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)


def http_server(config: Config, velox: Velox) -> HTTPServer:
    """
    Instantiates the VeloxSearch HTTP Server
    """
    # FIXME: Python http.server is not recommended for production
    # https://docs.python.org/3/library/http.server.html
    # Replace it with something else, for example uvicorn
    return VeloxHTTPServer(
        velox,
        (config.http_server.listen_addr, config.http_server.listen_port),
        VeloxHTTPRequestHandler,
    )


def main():
    """
    Entrypoint of VeloxSearch HTTP server
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Config file (in toml)")
    args = parser.parse_args()

    config = Config.load(args.config)

    logging.basicConfig(level=config.logging.level)
    logging.debug("Loaded configuration: %s", config)

    velox = Velox(config)

    httpd = http_server(config, velox)
    logging.info(
        "HTTP Server listening on %s:%d",
        config.http_server.listen_addr,
        config.http_server.listen_port,
    )

    httpd.serve_forever()
