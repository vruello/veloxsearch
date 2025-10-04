import logging
import os
import unittest

from velox_search.config import (
    Config,
    HttpServerConfig,
    LoggingConfig,
    SearchAlgorithm,
    SearchConfig,
)
from velox_search.velox import Velox


class TestVelox(unittest.TestCase):
    def _get_config(
        self, wordlist: str, algorithm: SearchAlgorithm, limit: int
    ) -> Config:
        return Config(
            http_server=HttpServerConfig(listen_addr="127.0.0.1", listen_port=10000),
            search=SearchConfig(
                wordlist=os.path.join(os.path.dirname(__file__), f"../data/{wordlist}"),
                algorithm=algorithm,
                limit=limit,
            ),
            logging=LoggingConfig(level="INFO"),
        )

    def test_search_cr_in_eff_large_wordlist(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(self._get_config("eff_large_wordlist.txt", algorithm, 10))
            except NotImplementedError:
                logging.warning("Algorithm %s is not implemented", algorithm)
                continue

            self.assertEqual(
                velox.search_prefix("cr"),
                [
                    "crabbing",
                    "crabgrass",
                    "crablike",
                    "crabmeat",
                    "cradle",
                    "cradling",
                    "crafter",
                    "craftily",
                    "craftsman",
                    "craftwork",
                ],
                msg=f"Algorithm {algorithm} failed",
            )

    def test_search_ab_in_gameofthrones(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(
                    self._get_config("gameofthrones_8k-2018.txt", algorithm, 10)
                )
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.search_prefix("ab"),
                [
                    "abandon",
                    "abandon",
                    "abandoning",
                    "abandoning",
                    "abilities",
                    "abilities",
                    "abject",
                    "abject",
                    "aboard",
                    "aboard",
                ],
                msg=f"Algorithm {algorithm} failed",
            )

    def test_search_ab_in_gameofthrones_5(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(
                    self._get_config("gameofthrones_8k-2018.txt", algorithm, 5)
                )
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.search_prefix("ab"),
                [
                    "abandon",
                    "abandon",
                    "abandoning",
                    "abandoning",
                    "abilities",
                ],
                msg=f"Algorithm {algorithm} failed",
            )

    def test_search_rockyou_cora(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(self._get_config("rockyou.txt", algorithm, 5))
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.search_prefix("cora"),
                ["cora", "cora carsyn", "cora#1", "cora$on", "cora&alec"],
                msg=f"Algorithm {algorithm} failed",
            )
