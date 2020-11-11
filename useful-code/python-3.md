# Python 3

These are blocks of code that can be useful for doing coding problems. They might be used as-is, or altered to suite a specific problem.

I'm currently translating all of my Java code into Python, so there's not as much here right now.

## <!-- omit in toc -->Contents

- [Disjoint Sets Data Structure](#disjoint-sets-data-structure)
- [Trie Data Structure](#trie-data-structure)

## Disjoint Sets Data Structure

This code uses path-compression and union by rank.

```python
class DSet:
    """A disjoint set.

    Attributes:
        parent (DSet): The DSet used to find the set's representative.
        rank (int): The maximum path length to a child DSet.
    """

    def __init__(self) -> None:
        """Inits DSet as a new set"""
        self.parent = self
        self.rank = 0


def find(x: DSet) -> DSet:
    """Finds a set's representative.

    Args:
        x (DSet): The disjoint set that we're searching for.

    Returns:
        DSet: The representative of the disjoint set.
    """

    if x is not x.parent:
        x.parent = find(x.parent)
    return x.parent


def union(a: DSet, b: DSet) -> None:
    """Unions two sets.

    Args:
        a (DSet): The first set to union.
        b (DSet): The second set to union.
    """

    a = find(a)
    b = find(b)
    if a is b:
        return
    if a.rank > b.rank:
        b.parent = a
    else:
        a.parent = b
        if a.rank == b.rank:
            b.rank += 1
```

[back to top](#python-3)

## Trie Data Structure

[source (the java code)](https://www.geeksforgeeks.org/trie-insert-and-search/)

```python
class Trie:
    """A trie data structure.

    Attributes:
        ALPHABET_SIZE (int): The size of the alphabet.
        root (Node): The root node of the trie.
    """

    ALPHABET_SIZE = 26

    def __init__(self) -> None:
        """Inits an empty Trie."""

        self.root = self.Node()

    def insert(self, pattern: str) -> None:
        """Inserts a pattern into this trie.

        Args:
            pattern (str): The pattern to be inserted.
        """

        crawl = self.root
        # crawl down the trie, creating new nodes as needed
        for c in pattern:
            child = self.index(c)
            if crawl.children[child] is None:
                crawl.children[child] = self.Node()
            crawl = crawl.children[child]
        # crawl is the last chr in pattern
        crawl.end_node = True

    def search(self, pattern: str) -> bool:
        """Finds a pattern in this trie.

        Args:
            pattern (str): The pattern to search for.

        Returns:
            bool: True if the pattern is in this trie.
        """

        crawl = self.root
        # crawl down the trie
        for c in pattern:
            child = self.index(c)
            # check if the chr exists
            if crawl.children[child] is None:
                return False
            crawl = crawl.children[child]
        # check if the last chr is in the pattern and is an end node
        return crawl is not None and crawl.end_node

    def index(self, c: chr) -> int:
        """Determines the index of a chr in a children array.

        Args:
            c (chr): The chr to index.

        Returns:
            int: The index of c in a children array.
        """

        return ord(c) - ord("a")

    class Node:
        """A node in a trie.

        Attributes:
            children (list[{Node, None}]): The characters that are children of
            this Node.
            end_node (bool): Indicates if this Node is the end of a pattern.
        """

        def __init__(self) -> None:
            """Inits an empty Node."""

            self.children = [None] * Trie.ALPHABET_SIZE
            self.end_node = False
```

[back to top](#python-3)
