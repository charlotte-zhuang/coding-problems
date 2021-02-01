"""Generate heap runtime tests.

Attributes:
    MIN_VAL (int): A default minimum key value.
    MAX_VAL (int): A default maximum key value.
"""

from pathlib import Path
import random
import heapq

MIN_VAL = int(-1e9)
MAX_VAL = int(1e9)


def random_test(
    test_data: Path,
    size: int = 1000,
    op: int = 1000000,
    addfreq: int = 1,
    decfreq: int = 8,
    popfreq: int = 1,
    minval: int = MIN_VAL,
    maxval: int = MAX_VAL,
) -> tuple[int]:
    """Generates random commands for a heap to execute.

    Args:
        test_data (Path): The file to write the test to.
        size (int): The initial heap size.
        op (int): The number of operations.
        addfreq (int): The weighted frequency of add operations.
        decfreq (int): The weighted frequency of decrease key operations.
        popfreq (int): The weighted frequency of pop min operations.
        minval (int): The minimum value to add to the heap.
        maxval (int): The maximum value to add to the heap.

    Returns:
        tuple[int]: (total operations, add operations, decrease key
            operations, pop minimum operations, minval, maxval)
    """

    totalfreq = addfreq + decfreq + popfreq
    arr = []
    heap = []
    add = 0
    dec = 0
    pop = 0
    with test_data.open(mode="w") as dat:
        for _ in range(size):
            num = random.randint(minval, maxval)
            heapq.heappush(heap, (num, len(arr)))
            arr.append(num)
            dat.write(f"a {num}\n")
            add += 1
        heapsize = size
        for _ in range(op):
            action = random.randint(0, totalfreq)
            if action < decfreq and heapsize != 0:
                # decrease key
                key, i = random.choice(heap)
                while arr[i] != key:
                    key, i = random.choice(heap)
                nk = random.randint(minval, key)
                heapq.heappush(heap, (nk, i))
                arr[i] = nk
                dat.write(f"d {i} {nk}\n")
                dec += 1
            elif action < decfreq + popfreq and heapsize != 0:
                # pop
                elem = heapq.heappop(heap)
                while arr[elem[1]] != elem[0]:
                    elem = heapq.heappop(heap)
                arr[elem[1]] = None
                heapsize -= 1
                dat.write("p\n")
                pop += 1
            else:
                # add
                num = random.randint(minval, maxval)
                heapq.heappush(heap, (num, len(arr)))
                arr.append(num)
                heapsize += 1
                dat.write(f"a {num}\n")
                add += 1
    total = size + op
    return total, add, dec, pop, minval, maxval
