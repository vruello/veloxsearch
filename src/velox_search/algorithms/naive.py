from . import Search


class NaiveSearch(Search):
    """
    Naive implementation using a simple unsorted list
    """

    wordlist: list[str]

    def load_wordlist(self, wordlist: str) -> None:
        with open(wordlist, "r", errors="replace") as fd:
            # Transform words in lowercase because the search is case insensitive
            self.wordlist = [word.strip().lower() for word in fd]

    def complete_prefix(self, prefix: str) -> list[str]:
        # Transform prefix in lowercase because the search in case insensitive
        prefix_lower = prefix.lower()

        # 1. We compute a set of words - to avoid duplicates - that start with the
        # given prefix
        # 2. We sort this set in lexicographic order
        # 3. We return only <self.config.limit> results
        matching = sorted(
            set(word for word in self.wordlist if word.startswith(prefix_lower))
        )

        return matching[: self.config.limit]
