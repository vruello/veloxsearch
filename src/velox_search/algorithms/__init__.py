from velox_search.config import SearchConfig


class Search:
    config: SearchConfig

    def __init__(self, config: SearchConfig):
        self.config = config

    def load_wordlist(self, wordlist: str) -> None:
        raise NotImplementedError

    def search_prefix(self, prefix: str) -> list[str]:
        raise NotImplementedError
