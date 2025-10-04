from . import Search


class NaiveSearch(Search):
    """
    Naive implementation using a simple unsorted list
    """

    wordlist: list[str]

    def load_wordlist(self, wordlist: str) -> None:
        with open(wordlist, "r") as fd:
            self.wordlist = [line.strip() for line in fd.readlines()]

    def search_prefix(self, prefix: str) -> list[str]:
        matching = sorted(word for word in self.wordlist if word.startswith(prefix))

        return matching[: self.config.limit]
