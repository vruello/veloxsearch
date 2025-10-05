from . import Search
import bisect


class BisectSearch(Search):
    """
    Use a sorted list and a bisection algorithm
    """

    wordlist: list[str]

    def load_wordlist(self, wordlist: str) -> None:
        with open(wordlist, "r", errors="replace") as fd:
            # We need the list to be sorted
            # Transform words in lowercase because search is case insensitive
            self.wordlist = sorted(line.strip().lower() for line in fd.readlines())

    def complete_prefix(self, prefix: str) -> list[str]:
        # Transform prefix in lowercase because search is case insensitive
        prefix_lower = prefix.lower()

        # We can use bisect because wordlist is sorted
        # bisect_left gives the index where "<prefix_lower>" would be inserted
        # to keep <self.wordlist> sorted, meaning that all following words are >= <prefix>
        index = bisect.bisect_left(self.wordlist, prefix_lower)

        # We use a set to remove duplicates
        words: set[str] = set()
        while (len(words) < self.config.limit
               and self.wordlist[index].startswith(prefix_lower)):
            # We take at most <self.config.limit> unique words that starts with <prefix>
            words.add(self.wordlist[index])
            index += 1

        # The set items need to be sorted again
        return sorted(words)
