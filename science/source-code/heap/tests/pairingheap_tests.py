import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute()))

import random
import heapq
from heap import pairingheap

MIN_VAL = int(-1e9)
MAX_VAL = int(1e9)


def remove_test(
    size: int = 10000, rep: int = 1000, minval: int = MIN_VAL, maxval: int = MAX_VAL
) -> bool:
    """Tests the remove operation.

    Args:
        size (int): The size of the test heap.
        rep (int): The repetitions of remove operations.
        minval (int): The minimum value to be added.
        maxval (int): The maximum value to be added.

    Raises:
        AssertionError: Test failed.
    """

    binary_heap = []
    pairing_heap = pairingheap.Heap()
    nodes = set()
    removed = set()
    for i in range(size):
        num = random.randint(minval, maxval)
        heapq.heappush(binary_heap, (num, i))
        nodes.add((pairing_heap.add(num), i))
    for i in range(rep):
        rem = random.choice(tuple(nodes))
        nodes.remove(rem)
        pairing_heap.remove(rem[0])
        removed.add(rem[1])
        assert pairing_heap.size == size - i - 1, "Failed remove node: size mismatch"
    while binary_heap:
        exp = heapq.heappop(binary_heap)
        while binary_heap and exp[1] in removed:
            exp = heapq.heappop(binary_heap)
        if not exp[1] in removed:
            act = pairing_heap.pop()
            assert exp[0] == act.key, "Failed removal test: value mismatch"
    assert pairing_heap.root == None, "Failed removal test: heap not empty"


def decrease_test(
    size: int = 1000, rep: int = 10000, minval: int = MIN_VAL, maxval: int = MAX_VAL
) -> None:
    """Tests the decrease key operation.

    Args:
        size (int): The size of the test heap. Must be greater than 0.
        rep (int): The repetitions of decrease key operations.
        minval (int): The minimum value to be added.
        maxval (int): The maximum value to be added.

    Raises:
        AssertionError: Test failed.
    """

    binary_heap = []
    pairing_heap = pairingheap.Heap()
    nodes = []
    arr = []
    for i in range(size):
        num = random.randint(minval, maxval)
        heapq.heappush(binary_heap, (num, i))
        nodes.append(pairing_heap.add(num))
        arr.append(num)
    for _ in range(rep):
        i = random.randint(0, size - 1)
        node = nodes[i]
        key = random.randint(minval, node.key)
        pairing_heap.decreasekey(node, key)
        heapq.heappush(binary_heap, (key, i))
        arr[i] = key
    while binary_heap:
        exp = heapq.heappop(binary_heap)
        while binary_heap and arr[exp[1]] != exp[0]:
            exp = heapq.heappop(binary_heap)
        if arr[exp[1]] == exp[0]:
            arr[exp[1]] = -1
            act = pairing_heap.pop()
            assert exp[0] == act.key, "Failed decrease key test: value mismatch"
    assert pairing_heap.root == None, "Failed decrease key test: heap not empty"


def heap_test(
    rep: int = 10000,
    addfreq: int = 1,
    popfreq: int = 1,
    minval: int = MIN_VAL,
    maxval: int = MAX_VAL,
) -> None:
    """Tests add and pop operations.

    Args:
        rep (int): The repetitions of add/pop operations.
        addfreq (int): The weighted frequency of add operations.
        popfreq (int): The weighted frequency of pop operations.
        minval (int): The minimum value to be added.
        maxval (int): The maximum value to be added.

    Raises:
        AssertionError: Test failed.
    """

    totalfreq = addfreq + popfreq
    binary_heap = []
    pairing_heap = pairingheap.Heap()
    for _ in range(rep):
        add = random.randint(0, totalfreq) < addfreq
        if add or len(binary_heap) == 0:
            num = random.randint(minval, maxval)
            heapq.heappush(binary_heap, num)
            pairing_heap.add(num)
            assert (
                binary_heap[0] == pairing_heap.root.key
            ), "Failed add operation: min value mismatch"
        else:
            a = heapq.heappop(binary_heap)
            b = pairing_heap.pop().key
            assert a == b, "Failed pop operation: value mismatch"
            if binary_heap:
                assert (
                    binary_heap[0] == pairing_heap.root.key
                ), "Failed pop operation: new min value mismatch"
            else:
                assert pairing_heap.root == None, "Failed pop operation: heap not empty"
        assert (
            len(binary_heap) == pairing_heap.size
        ), "Failed add or pop operation: heap size mismatch"


if __name__ == "__main__":
    heap_test()
    decrease_test()
    remove_test()
    remove_test(size=1000, rep=1000)
    print("Pairing heap passed all tests")
