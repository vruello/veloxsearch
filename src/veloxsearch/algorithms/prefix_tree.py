from typing import Optional
from . import Search


class Node:
    children: dict[str, "Node"]
    # A node is a leaf if it represents a word in the list
    is_leaf: bool

    def __init__(self):
        self.children = {}
        self.is_leaf = False

    def __str__(self) -> str:
        children = (f"{key}:{value}" for key, value in self.children.items())
        return f"Node(is_leaf={self.is_leaf},children={{{','.join(children)}}})"


class Tree:
    def __init__(self) -> None:
        self.root = Node()

    def __str__(self) -> str:
        return f"Tree({str(self.root)})"

    def insert(self, word: str) -> None:
        """
        Insert a word in the tree
        """
        node = self.root
        for char in word:
            if char not in node.children:
                # A node does not exist yet for this char
                node.children[char] = Node()
            node = node.children[char]

        node.is_leaf = True

    def _find_prefix_node(self, prefix: str) -> Optional[Node]:
        """
        Try to find the node that represents the prefix
        Return None if the prefix is unknown, return the node otherwise
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_all_words(
        self, node: Node, current_word: str, words: list, limit: int
    ) -> None:
        """
        Fill the <words> list by doing a depth first search starting with node <node>.
        At most <limit> words will be taken, sorted in lexicographic order
        """
        if len(words) >= limit:
            return

        # If the current node is a leaf, we add current word to <words>
        if node.is_leaf:
            words.append(current_word)

        # Recursively call for each child node, in lexicographic order
        # while the limit has not been passed
        for char, child_node in sorted(node.children.items()):
            if len(words) >= limit:
                return

            self._collect_all_words(child_node, current_word + char, words, limit)

    def complete_prefix(self, prefix: str, limit: int) -> list[str]:
        """
        Return a list of maximum <limit> words starting with the given prefix <prefix>
        sorted by lexicographic order
        """
        # Find the node corresponding to the prefix
        start_node = self._find_prefix_node(prefix)

        if start_node is None:
            # The prefix is unknown, so there is no words
            return []

        # Retrieve words under <start_node>
        words: list[str] = []
        self._collect_all_words(start_node, prefix, words, limit)

        return words


class PrefixTreeSearch(Search):
    """
    Use a prefix tree to index wordlist
    """

    def load_wordlist(self, wordlist: str) -> None:
        self.tree = Tree()
        with open(wordlist, "r", errors="replace") as fd:
            for word in fd:
                # Transform words in lowercase because search is case insensitive
                self.tree.insert(word.strip().lower())

    def complete_prefix(self, prefix: str) -> list[str]:
        # Transform prefix in lowercase because search is case insensitive
        return self.tree.complete_prefix(prefix.lower(), self.config.limit)
