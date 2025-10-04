from velox_search.config import SearchConfig


class Search:
    """
    Base class for search algorithms
    """

    config: SearchConfig

    def __init__(self, config: SearchConfig):
        self.config = config

    def load_wordlist(self, wordlist: str) -> None:
        """
        Load the wordlist in memory
        """
        raise NotImplementedError

    def search_prefix(self, prefix: str) -> list[str]:
        """
        Return a list of words matching the given prefix in alphabetical order
        """
        raise NotImplementedError
