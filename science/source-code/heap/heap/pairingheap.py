#!/usr/bin/env python3.9

import math


class HeapNode:
    """A node in a pairing heap.

    Attributes:
        key (int): The key value stored by this node. Guaranteed to be less
            than or equal to all keys in this subheap.
        left (HeapNode or None): The child of the node.
        right (HeapNode or None): The sibling of the node.
        parent (HeapNode or None): The parent of the node.
    """

    def __init__(self, key: int) -> None:
        """Inits a solitary node of a heap.

        Args:
            key (int): The key stored in the node.
        """

        self.key = key
        self.left = None
        self.right = None
        self.parent = None

    def cut(self) -> None:
        """Cuts the node from its parent. Parent must not be None."""

        if self.parent.left == self:
            self.parent.left = self.right
        else:
            self.parent.right = self.right
        if self.right:
            self.right.parent = self.parent
        self.parent = None
        self.right = None


class Heap:
    """A minheap implemented using a pairing heap.

    Attributes:
        root (HeapNode or None): The node containing the minimum key in the
            heap.
        size (int): The size of the heap.
    """

    def __init__(self) -> None:
        """Inits an empty minheap."""

        self.root = None
        self.size = 0

    @staticmethod
    def meld(a: HeapNode, b: HeapNode) -> HeapNode:
        """Melds two trees together.

        Args:
            a (HeapNode): A disjoint tree.
            b (HeapNode): A disjoint tree.

        Returns:
            HeapNode: The root of the combined tree.
        """

        if a.key > b.key:
            a, b = b, a
        b.parent = a
        if a.left:
            b.right = a.left
            b.right.parent = b
        a.left = b
        return a

    def add(self, key: int) -> HeapNode:
        """Adds a key to the heap.

        Args:
            key (int): The key to add.

        Returns:
            HeapNode: The node that stores the key.
        """

        node = HeapNode(key)
        if not self.root:
            self.root = node
        else:
            self.root = self.meld(self.root, node)
        self.size += 1
        return node

    def pop(self) -> HeapNode:
        """Returns and removes the minimum node in this heap.

        Returns:
            HeapNode or None: The node with the minimum key. None if the
                heap is empty.
        """

        res = self.root
        if not res:
            return res
        self.size -= 1
        if not res.left:
            self.root = None
            return res
        # link pairs of subtrees by their roots
        crawl = res.left
        res.left = None
        roots = []
        while crawl and crawl.right:
            a = crawl
            b = crawl.right
            crawl = b.right
            a.right = None
            b.right = None
            roots.append(self.meld(a, b))
        if crawl:
            crawl.right = None
            roots.append(crawl)
        # link all pairs together to make one tree
        self.root = roots.pop()
        for node in reversed(roots):
            self.root = self.meld(self.root, node)
        self.root.parent = None
        return res

    def decreasekey(self, node: HeapNode, key: int) -> HeapNode:
        """Decreases the key stored in a node.

        Args:
            node (HeapNode): The node to decrease.
            key (int): The new key for the node. Must be less than the
                original key.

        Returns:
            HeapNode: The decreased node.
        """

        # if node.key < key:
        #     raise ValueError("Cannot increase key")
        node.key = key
        if not node.parent or node.parent.key <= key:
            return node
        node.cut()
        self.root = self.meld(self.root, node)
        return node

    def remove(self, node: HeapNode) -> HeapNode:
        """Removes a node from the heap.

        Args:
            node (HeapNode): The node to remove.

        Returns:
            HeapNode: The removed node.
        """

        self.decreasekey(node, -math.inf)
        return self.pop()
