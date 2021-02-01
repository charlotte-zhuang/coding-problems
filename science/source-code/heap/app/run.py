"""Conduct runtime tests on heaps."""

import sys
from pathlib import Path
import timeit
import heapq

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from heap import pairingheap, fibonacciheap


def pairing_time(testdata: Path) -> float:
    """Executes the test using a pairing heap.

    Args:
        test_data (Path): The file to write the test to.

    Returns:
        float: The execution time in seconds.
    """

    size, ops = read_operations(testdata)
    start = timeit.default_timer()
    heap = pairingheap.Heap()
    nodes = [None] * size
    np = 0
    for o in ops:
        if o[0] == "a":
            nodes[np] = heap.add(o[1])
            np += 1
        elif o[0] == "d":
            heap.decreasekey(nodes[o[1]], o[2])
        else:
            heap.pop()
    stop = timeit.default_timer()
    return stop - start


def fibonacci_time(testdata: Path) -> float:
    """Executes the test using a Fibonacci heap.

    Args:
        test_data (Path): The file to write the test to.

    Returns:
        float: The execution time in seconds.
    """

    size, ops = read_operations(testdata)
    start = timeit.default_timer()
    heap = fibonacciheap.Heap()
    nodes = [None] * size
    np = 0
    for o in ops:
        if o[0] == "d":
            heap.decreasekey(nodes[o[1]], o[2])
        elif o[0] == "a":
            nodes[np] = heap.add(o[1])
            np += 1
        else:
            heap.pop()
    stop = timeit.default_timer()
    return stop - start


def binary_time(testdata: Path) -> float:
    """Executes the test using a pairing heap.

    Args:
        test_data (Path): The file to write the test to.

    Returns:
        float: The execution time in seconds.
    """

    size, ops = read_operations(testdata)
    start = timeit.default_timer()
    heap = []
    arr = [None] * size
    np = 0
    for o in ops:
        if o[0] == "d":
            arr[o[1]] = o[2]
            heapq.heappush(heap, (o[2], o[1]))
            while arr[heap[0][1]] != heap[0][0]:
                heapq.heappop(heap)
        elif o[0] == "a":
            heapq.heappush(heap, (o[1], np))
            arr[np] = o[1]
            np += 1
        else:
            elem = heapq.heappop(heap)
            while arr[elem[1]] != elem[0]:
                elem = heapq.heappop(heap)
            arr[elem[1]] = None
    stop = timeit.default_timer()
    return stop - start


def read_operations(testdata: Path) -> tuple[int, list[tuple]]:
    """Reads the test data from the file.

    Args:
        test_data (Path): The file to write the test to.

    Returns:
        tuple[int, list[tuple]]: First value is the number of add operations.
            Second value is a list of all commands in the following form:

            ("d", index, amt) decrease key at the index by an amount
            ("a", key) add key
            ("p") pop minimum
    """

    add = 0
    ops = []
    with testdata.open(mode="r") as dat:
        for line in dat:
            line = line.split()
            if line[0] == "d":
                ops.append(("d", int(line[1]), int(line[2])))
            elif line[0] == "a":
                ops.append(("a", int(line[1])))
                add += 1
            else:
                ops.append(("p"))
    return add, ops
