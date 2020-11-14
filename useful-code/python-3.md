# Python 3

These are blocks of code that can be useful for doing coding problems. They might be used as-is, or altered to suite a specific problem.

I'm currently translating all of my Java code into Python, so there's not as much here right now.

## <!-- omit in toc -->Contents

- [Disjoint Sets Data Structure](#disjoint-sets-data-structure)
- [Trees](#trees)
  - [Trie Data Structure](#trie-data-structure)
  - [Fenwick Tree](#fenwick-tree)

## Disjoint Sets Data Structure

Useful for keeping track of sets of disjoint elements, and performing unions between sets. Time-complexity is _Θ(m lg\*(n))_, where _m_ is the number of operations and _n_ is the number of sets.

This code uses path-compression and union by rank.

```python
class DSet:
    """A disjoint set.

    Attributes:
        parent (DSet): The DSet used to find the set's representative.
        rank (int): The maximum path length to a child DSet.
    """

    def __init__(self) -> None:
        """Inits DSet as a new set."""

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

## Trees

### Trie Data Structure

Used to store a dictionary of patterns. Time-complexity is linear in the length of the pattern.

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

### Fenwick Tree

A binary indexed tree. Useful for finding the sum of a range of values in an array in logarithmic time. Each node in the tree stores the sum within a range from the index down to the index minus the smallest set bit in the index's binary representation.

> Example  
> 10 = 0b1010  
> 2 = 0b0010  
> 10 - 2 = 8  
> tree[10] = sum of values[9..10]

```python
class Fenwick_Tree:
    """A Fenwick Tree (Binary Indexed Tree).

    Attributes:
        values (list[int]): The list of values.
        tree (list[int]): The Fenwick Tree. Indexes are offset by 1.
    """

    def __init__(self, size: int) -> None:
        """Inits a fenwick tree with all zero values.

        Args:
            size (int): The number of values in the tree.
        """

        self.values = [False] * size
        self.tree = [0] * (size + 1)

    @classmethod
    def from_list(cls, values: list[int]) -> object:
        """Inits a fenwick tree from a list of values.

        Args:
            values (list[int]): The list of values to store in the tree.

        Returns:
            object: The fenwick tree.
        """

        fenwick_tree = cls(len(values))
        # add all elements from values to the tree
        for i, value in enumerate(values):
            fenwick_tree.update(i, value)
        return fenwick_tree

    def update(self, index: int, value: int) -> None:
        """Updates the value of an index.

        Args:
            index (int): The index to be updated.
            value (int): The value to update the index to.
        """

        dif = value - self.values[index]
        self.values[index] = value
        # update the value of the index and all successors
        index += 1
        while index < len(self.tree):
            self.tree[index] += dif
            index += index & (-index)

    def count(self, index: int) -> int:
        """Counts values up to an index.

        Args:
            index (int): The last index to include in the count.

        Returns:
            int: The sum of values in the range [0 : index].
        """

        count = 0
        # add the value of the index and all ancestors
        index += 1
        while index > 0:
            count += self.tree[index]
            index -= index & (-index)
        return count
```

[back to top](#python-3)
