from velox_search.algorithms import Search
from velox_search.algorithms.naive import NaiveSearch
from velox_search.config import Config, SearchAlgorithm


class Velox:
    """
    Main class of Velox

    During initialization, it instantiates the appropriate search class and
    load the configured wordlist.
    """

    config: Config
    loaded: bool
    handler: Search

    def __init__(self, config: Config) -> None:
        self.config = config

        match config.search.algorithm:
            case SearchAlgorithm.Naive:
                self.handler = NaiveSearch(config.search)
            case _:
                raise NotImplementedError

        self.handler.load_wordlist(config.search.wordlist)

    def search_prefix(self, prefix: str) -> list[str]:
        """
        Return a list of words matching the provided prefix
        """
        return self.handler.search_prefix(prefix)
