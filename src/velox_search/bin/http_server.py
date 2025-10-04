from http import HTTPStatus
from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer,
    ThreadingHTTPServer,
)
import logging
import argparse
import json
import urllib.parse

from ..config import Config


class VeloxHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""
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
        if query is None:
            # Missing argument
            self.send_response(HTTPStatus.UNPROCESSABLE_CONTENT)
            self.flush_headers()
            return

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"query": query}).encode())


def http_server(config: Config) -> HTTPServer:
    """
    Instantiates the VeloxSearch HTTP Server
    """
    # FIXME: Python http.server is not recommended for production
    # https://docs.python.org/3/library/http.server.html
    # Replace it with uvicorn
    return ThreadingHTTPServer(
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

    httpd = http_server(config)
    logging.info(
        "HTTP Server listening on %s:%d",
        config.http_server.listen_addr,
        config.http_server.listen_port,
    )

    httpd.serve_forever()
