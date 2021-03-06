# Python 3

These are blocks of code that can be useful for doing coding problems. They might be used as-is, or altered to suite a specific problem.

I'm currently translating all of my Java code into Python, so there's not as much here right now.

## <!-- omit in toc -->Contents

- [Factoring](#factoring)
  - [Greatest Common Divisor](#greatest-common-divisor)
  - [Prime Factorization](#prime-factorization)
  - [Prove Primality](#prove-primality)
  - [Miller-Rabin Primality Test](#miller-rabin-primality-test)
- [Disjoint Sets Data Structure](#disjoint-sets-data-structure)
- [Trees](#trees)
  - [Trie Data Structure](#trie-data-structure)
  - [Fenwick Tree](#fenwick-tree)

## Factoring

### Greatest Common Divisor

[Source](https://en.wikipedia.org/wiki/Euclidean_algorithm)

```python
def gcd(a: int, b: int) -> int:
    """Finds the greatest common divisor of two integers using the Euclidean
        division algorithm.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The GCD of a and b.
    """

    # a holds the last-last remainder of a % b
    # b hold the last remainder of a % b
    while b != 0:
        a, b = b, a % b
    # stop when a % b == 0
    return a
```

### Prime Factorization

Repeatedly divides a given number to count the factors. Time-complexity is _O(n^0.5)_, where _n_ is the size of the factored number.

It can greatly benefit from a fast prime check, to see if a number has any factors (see below).

```python
def prime_factors(num: int) -> list[tuple[int]]:
    """Finds all prime factors of a number

    Args:
        num (int): The number to prime factorize.

    Returns:
        list[tuple[int]]: A list of factors from least to greatest in tuple form: (factor, power)
    """

    factors = []
    # return numbers that are too small
    if num < 4:
        factors.append((num, 1))
        return factors
    # add the number of twos that divide num
    if (num & 1) == 0:
        power = 0
        while (num & 1) == 0:
            power += 1
            num >>= 1
        factors.append((2, power))
        if num == 1:
            return factors
    # num must be odd
    limit = num ** 0.5 + 1
    pf = 3
    while pf < limit:
        if num % pf == 0:
            power = 0
            while num % pf == 0:
                power += 1
                num //= pf
            factors.append((pf, power))
            if num == 1:
                return factors
            limit = num ** 0.5 + 1
        pf += 2
    # num is a prime greater than 2
    factors.append((num, 1))
    return factors
```

[back to top](#python-3)

### Prove Primality

The only way to prove that a number is prime is to check smaller numbers for factors. The time-complexity is _O(n^0.5)_. There are shortcuts that can be taken for [special cases](https://en.wikipedia.org/wiki/Primality_test), and probabilistic primality tests perform much better.

```python
def primality(num: int) -> bool:
    """Checks if a number is prime.

    Args:
        num (int): The number to check for primality.

    Returns:
        bool: Whether the number is prime.
    """

    if num % 2 == 0:
        return num == 2
    if num < 2:
        return False
    # check for factors up to the square root of num
    for f in range(3, int(num ** 0.5)):
        if num % f == 0:
            return False
    return True
```

[back to top](#python-3)

### Miller-Rabin Primality Test

This is a probabilistic primality test. It will always detect a prime number (no false negatives), but has a false positive rate of at most _4^-k_, where _k_ is the number of repetitions that the test is performed. For large numbers, the accuracy improves to _8^-k_. Time-complexity is _O(k lg^3(n))_, where _k_ is the number of repetitions and _n_ is the tested number.

Performance can be improved by using [specific witnesses](https://en.wikipedia.org/wiki/Miller–Rabin_primality_test#Testing_against_small_sets_of_bases) rather than random ones.

Sources: [Wikipedia](https://en.wikipedia.org/wiki/Miller–Rabin_primality_test), [GeeksforGeeks](https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/?ref=lbp)

```python
def primality_test(num: int, rep: int) -> bool:
    """Performs the Miller-Rabin primality test to determine if a number is a
        probable prime.

    Args:
        num (int): The number to test for primality.
        rep (int): The number of repetitions to perform the test.

    Returns:
        bool: True if the number is a probable prime. False if the number is
            composite.
    """

    # handle small cases
    if num % 2 == 0:
        return num == 2
    if num < 9:
        return num > 1
    # find d by factoring out all powers of 2
    d = num - 1
    r = 0
    while d & 1 == 0:
        d >>= 1
        r += 1
    # repeat the test for the specified number of repetitions
    for _ in range(rep):
        if not test_witness(num, d, r):
            return False
    # num is a probable prime
    return True


def test_witness(num: int, d: int, r: int) -> bool:
    """Tests a number for the Miller-Rabin primality test with a random
        witness.

    Args:
        num (int): The number to test for primality.
        d (int): The number (num - 1) with all powers of 2 removed.
        r (int): The power of 2 removed to make d, (2 ** r * d == num - 1)

    Returns:
        bool: Whether the number passed the test.
    """

    a = random.randint(2, num - 2)
    x = mod_pow(a, d, num)
    if x == 1 or x + 1 == num:
        return True
    for _ in range(r - 1):
        x = x * x % num
        if x + 1 == num:
            return True
        # check if x won't change
        if x == 1:
            break
    return False


def mod_pow(base: int, exp: int, mod: int) -> int:
    """Performs exponentiation with modulo.

    Args:
        base (int): The number to exponentiate.
        exp (int): The exponent.
        mod (int): The modulo number.

    Returns:
        int: The result, (base ** exp % mod)
    """

    res = 1
    base %= mod
    while exp > 0:
        # multiply res if exp is odd
        if exp & 1 == 1:
            res = res * base % mod
        # square the base if exp is even
        exp >>= 1
        base = base * base % mod
    return res
```

[back to top](#python-3)

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
        crawl.isend = True

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
        return crawl is not None and crawl.isend

    @staticmethod
    def index(c: chr) -> int:
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
            isend (bool): Indicates if this Node is the end of a pattern.
        """

        def __init__(self) -> None:
            """Inits an empty Node."""

            self.children = [None] * Trie.ALPHABET_SIZE
            self.isend = False
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

        self.values = [0] * size
        self.tree = [0] * (size + 1)

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
