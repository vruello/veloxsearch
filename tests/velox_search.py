from http.client import HTTPResponse
import logging
import unittest
import threading
import time
import random
import urllib.request
import urllib.error

from velox_search.bin.http_server import http_server
from velox_search.config import (
    Config,
    HttpServerConfig,
    LoggingConfig,
    SearchAlgorithm,
    SearchConfig,
)


class TestVeloxSearch(unittest.TestCase):
    """
    Integration tests of Velox Search HTTP Server
    """

    @classmethod
    def setUpClass(cls):
        """
        Start VeloxSearch HTTP Server with a dummy config
        """
        cls.listen_port = random.randint(11000, 13000)
        config = Config(
            http_server=HttpServerConfig(
                listen_addr="127.0.0.1", listen_port=cls.listen_port
            ),
            search=SearchConfig(
                wordlist="../data/eff_large_wordlist.txt",
                algorithm=SearchAlgorithm.Naive,
                limit=10,
            ),
            logging=LoggingConfig(level="INFO"),
        )
        cls.base_url = f"http://127.0.0.1:{cls.listen_port}"
        cls.httpd = http_server(config)

        cls.http_server_thread = threading.Thread(target=cls.httpd.serve_forever)
        # Force the thread to stop when main thread exits
        cls.http_server_thread.daemon = True
        cls.http_server_thread.start()

        logging.debug(
            f"HTTP Server starting in thread {cls.http_server_thread.ident}..."
        )
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        """
        Stop HTTP server
        """
        logging.debug("Stopping HTTP Server")
        cls.httpd.shutdown()
        # Wait for the HTTP server thread to exit
        cls.http_server_thread.join()
        logging.debug("HTTP Server stopped")

    def _make_request(self, path: str) -> HTTPResponse:
        """
        A helper to make a GET request and handle connection errors gracefully.
        """
        url = f"{self.base_url}{path}"
        return urllib.request.urlopen(url, timeout=2)

    def test_autocomplete_crypt(self):
        url = "/autocomplete?query=crypt"
        response = self._make_request(url)

        self.assertEqual(response.status, 200)
        content = response.read().decode("utf-8")

        # FIXME: test content

    def test_404(self):
        url = "/unknown"
        with self.assertRaises(urllib.error.HTTPError) as error:
            response = self._make_request(url)
        self.assertEqual(error.exception.code, 404)


# Pour lancer les tests depuis la ligne de commande: python -m unittest test_integration.py
if __name__ == "__main__":
    unittest.main()
