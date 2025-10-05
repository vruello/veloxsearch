from abc import abstractmethod
from veloxsearch.config import SearchConfig


class Search:
    """
    Base class for search algorithms
    """

    config: SearchConfig

    def __init__(self, config: SearchConfig):
        self.config = config

    @abstractmethod
    def load_wordlist(self, wordlist: str) -> None:
        """
        Load the wordlist in memory
        """
        raise NotImplementedError

    @abstractmethod
    def complete_prefix(self, prefix: str) -> list[str]:
        """
        Return a list of words starting with the given prefix in alphabetical order
        """
        raise NotImplementedError
