import logging
import unittest

from .utils import get_config
from velox_search.config import (
    SearchAlgorithm,
)
from velox_search.velox import Velox


class TestVelox(unittest.TestCase):
    def test_search_cr_in_eff_large_wordlist(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(get_config("eff_large_wordlist.txt", algorithm, 10))
            except NotImplementedError:
                logging.warning("Algorithm %s is not implemented", algorithm)
                continue

            self.assertEqual(
                velox.complete_prefix("cr"),
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

    def test_search_ab_in_gameofthrones_10(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(get_config("gameofthrones_8k-2018.txt", algorithm, 10))
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.complete_prefix("ab"),
                [
                    "abandon",
                    "abandoning",
                    "abilities",
                    "abject",
                    "aboard",
                    "about",
                    "above",
                    "absence",
                    "absent",
                    "abusing",
                ],
                msg=f"Algorithm {algorithm} failed",
            )

    def test_search_ab_in_gameofthrones_5(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(get_config("gameofthrones_8k-2018.txt", algorithm, 5))
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.complete_prefix("ab"),
                [
                    "abandon",
                    "abandoning",
                    "abilities",
                    "abject",
                    "aboard",
                ],
                msg=f"Algorithm {algorithm} failed",
            )

    def test_search_ab_in_gameofthrones_100(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(get_config("gameofthrones_8k-2018.txt", algorithm, 100))
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.complete_prefix("ab"),
                [
                    "abandon",
                    "abandoning",
                    "abilities",
                    "abject",
                    "aboard",
                    "about",
                    "above",
                    "absence",
                    "absent",
                    "abusing",
                ],
                msg=f"Algorithm {algorithm} failed",
            )

    def test_search_rockyou_cora(self):
        for algorithm in SearchAlgorithm:
            # PrefixTree takes too much time to load data
            if algorithm == SearchAlgorithm.PrefixTree:
                continue
            try:
                velox = Velox(get_config("rockyou.txt", algorithm, 5))
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.complete_prefix("cora"),
                ["cora", "cora carsyn", "cora#1", "cora$on", "cora&alec"],
                msg=f"Algorithm {algorithm} failed",
            )

    def test_search_french_pia(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(get_config("french.txt", algorithm, 7))
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.complete_prefix("pia"),
                [
                    "piaculaire",
                    "piaculaires",
                    "piaf",
                    "piaffa",
                    "piaffai",
                    "piaffaient",
                    "piaffais",
                ],
                msg=f"Algorithm {algorithm} failed",
            )

    def test_search_starwars_obi_3(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(get_config("starwars_8k_2018.txt", algorithm, 3))
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.complete_prefix("obi"),
                ["obi-wan"],
                msg=f"Algorithm {algorithm} failed",
            )

    def test_search_starwars_cor(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(get_config("starwars_8k_2018.txt", algorithm, 5))
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.complete_prefix("cor"),
                ["core", "corellia", "cornered", "corners", "corporate"],
                msg=f"Algorithm {algorithm} failed",
            )

    def test_search_harrypoter_bladiboulgou(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(
                    get_config("harrypotter_8k_3column-txt.txt", algorithm, 5)
                )
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.complete_prefix("bladiboulgou"),
                [],
                msg=f"Algorithm {algorithm} failed",
            )

    def test_search_french_with_accent(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(get_config("french.txt", algorithm, 3))
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.complete_prefix("abâ"),
                ["abâtardi", "abâtardie", "abâtardies"],
                msg=f"Algorithm {algorithm} failed",
            )

    def test_search_french_end_of_list(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(get_config("french.txt", algorithm, 10))
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.complete_prefix("zyth"),
                ["zython", "zythons", "zythum", "zythums"],
                msg=f"Algorithm {algorithm} failed",
            )

    def test_search_french_start_of_list(self):
        for algorithm in SearchAlgorithm:
            try:
                velox = Velox(get_config("french.txt", algorithm, 10))
            except NotImplementedError:
                continue

            self.assertEqual(
                velox.complete_prefix("a"),
                [
                    "a",
                    "a-t-elle",
                    "a-t-il",
                    "a-t-on",
                    "abaissa",
                    "abaissable",
                    "abaissables",
                    "abaissai",
                    "abaissaient",
                    "abaissais",
                ],
                msg=f"Algorithm {algorithm} failed",
            )
