# Heaps

This is a work in progress to test the performance of different heap structures against each other.

Initial testing suggests that binary heaps are really good. With enough decrease key operations, pairing and Fibonacci heaps gain parity. Pairing heaps are consistently better than Fibonacci heaps.

## Heaps included

1. Binary
2. Fibonacci
3. Pairing

## Usage

1. Install Python 3.9, [website](https://www.python.org)
2. On Linux/Mac, give `heap/app/start.py` permission to execute with `chmod 755 <file>`
3. Run `heap/app/start.py`

```zsh
cd ./heap
chmod 755 ./app/start.py  # On Linux/Mac
./app/start.py
```

## About

### Binary Heap

The binary heap used is an implicit binary heap from Python's [heap queue module](https://docs.python.org/3/library/heapq.html).

### Pairing Heap

The following sources were very helpful to make my pairing heap.

1. [The Pairing Heap: A New Form of Self-Adjusting Heap](http://www.cs.cmu.edu/afs/cs.cmu.edu/user/sleator/www/papers/pairing-heaps.pdf)
2. [COS 423 Lecture 6, Robert E. Tarjan](https://www.cs.princeton.edu/courses/archive/spr11/cos423/Lectures/Heaps.pdf)

### Fibonacci Heap

Largely copied from _Introduction to Algorithms_ by Cormen et al., 2009.

## Documentation

The Python scripts have a lot of comments that hopefully explain what's going on. Here's the project structure and some notable files to get started (it's a mess, can someone show me how to make a Python app?).

- `app/` Contains the heap CLI runtime tester
  - `start.py` Starts the CLI app
- `config/` Contains config files used to generate tests
  - `example.txt` An example config file with instructions to make your own
- `data/` Contains generated test data
- `heap/` Contains code for the heaps
- `tests/` Contains automated tests for the heaps' functionality

## Future

1. Testing with an actual algorithm (e.g. Dijkstra's)
2. Redo these tests in C++
3. Test more heaps/priority queues
