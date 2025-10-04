import unittest
import tomllib

from velox_search.config import Config

# TODO: Add tests for other config parameters


class TestConfig(unittest.TestCase):
    def test_valid_config(self):
        valid_config = """
        [http_server]
        listen_addr = "localhost"
        listen_port = 10000

        [search]
        wordlist = "data/eff_large_wordlist.txt"
        algorithm = "naive"

        [logging]
        level = "debug"
        """
        data = tomllib.loads(valid_config)

        config = Config._load_dict(data)

        self.assertEqual(config.http_server.listen_addr, "localhost")
        self.assertEqual(config.http_server.listen_port, 10000)
        self.assertEqual(config.search.wordlist, "data/eff_large_wordlist.txt")
        self.assertEqual(config.search.algorithm, "naive")
        self.assertEqual(config.logging.level, "debug")

    def test_invalid_http_server_listen_addr(self):
        # Missing http_server.listen_addr
        valid_config = """
        [http_server]
        listen_port = 10000

        [search]
        wordlist = "data/eff_large_wordlist.txt"
        algorithm = "naive"

        [logging]
        level = "debug"
        """
        data = tomllib.loads(valid_config)

        with self.assertRaises(ValueError) as error:
            config = Config._load_dict(data)
        self.assertEqual(
            str(error.exception), "Missing or invalid value http_server.listen_addr"
        )

    def test_invalid_http_server(self):
        # Invalid http_server section
        valid_config = """
        http_server = "test"

        [search]
        wordlist = "data/eff_large_wordlist.txt"
        algorithm = "naive"

        [logging]
        level = "debug"
        """
        data = tomllib.loads(valid_config)

        with self.assertRaises(ValueError) as error:
            config = Config._load_dict(data)
        self.assertEqual(str(error.exception), "Invalid section [http_server]")


if __name__ == "__main__":
    unittest.main()
