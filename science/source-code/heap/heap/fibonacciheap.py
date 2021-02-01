from __future__ import annotations
import math

PHI = (1 + 5 ** 0.5) / 2


class HeapNode:
    """A node in a Fibonacci heap.

    Attributes:
        key (int): The key value stored by this node. Guaranteed to be less
            than or equal to all keys in this subheap.
        parent (HeapNode or None): The parent of the node.
        child (HeapNode or None): An arbitrary child of the node.
        left (HeapNode): The left sibling of this node. Creates a circular
            linked list.
        right (HeapNode): The right sibling of this node. Creates a circular
            linked list.
        degree (int): The height of this node.
        marked (bool): Whether this node lost a direct child. False if this
            node is a root.
    """

    def __init__(self, key: int) -> None:
        """Inits a solitary node of a heap.

        Args:
            key (int): The key stored in the node.
        """

        self.key = key
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.degree = 0
        self.marked = False

    def addleft(self, node: HeapNode) -> None:
        """Merges another node with this node. Merging happens to the left
            and maintains a circular linked list.

        Args:
            node (HeapNode): The node to merge with.
        """

        node.right.left = self.left
        self.left.right = node.right
        self.left = node
        node.right = self

    def extract(self) -> None:
        """Extracts this node from its siblings' linked list."""

        self.right.left = self.left
        self.left.right = self.right
        self.left = self
        self.right = self


class Heap:
    """A Fibonacci heap.

    Attributes:
        minroot (HeapNode or None): The minimum node in the heap.
        size (int): The number of nodes in the heap.
    """

    def __init__(self) -> None:
        """Inits an empty heap."""

        self.minroot = None
        self.size = 0

    def add(self, key: int) -> HeapNode:
        """Adds a key into the heap.

        Args:
            key (int): The key to be added.

        Returns:
            HeapNode: The node containing the key.
        """

        node = HeapNode(key)
        if self.minroot:
            self.minroot.addleft(node)
            if key < self.minroot.key:
                self.minroot = node
        else:
            self.minroot = node
        self.size += 1
        return node

    def union(self, heap: Heap) -> Heap:
        """Unions another heap with this heap.

        Args:
            heap (Heap): The heap to union with.

        Returns:
            Heap: The unioned heap.
        """

        if not heap.minroot:
            return self
        self.minroot.addleft(heap.minroot)
        if heap.minroot.key < self.minroot.key:
            self.minroot = heap.minroot
        self.size += heap.size
        return self

    def pop(self) -> HeapNode:
        """Returns and removes the minimum node in this heap.

        Returns:
            HeapNode or None: The node with the minimum key. None if the
                heap is empty.
        """

        res = self.minroot
        if not res:
            return res
        # move child nodes to root list
        if res.child:
            res.addleft(res.child)
            res.child = None
        elif res.left == res:
            self.minroot = None
            self.size = 0
            return res
        # consolidate roots
        self.minroot = res.left
        res.extract()
        self.consolidate()
        self.size -= 1
        return res

    def consolidate(self) -> None:
        """Consolidates the roots of the heap after a pop operation. Also
        Fixes the parent reference of the root nodes.
        """

        deg = [None] * (int(math.log(self.size, PHI)) + 1)
        p = self.minroot
        last = p.right
        loop = True
        # combine roots with equal degrees
        while loop:
            if p == last:
                loop = False
            np = p.left
            while deg[p.degree]:
                q = deg[p.degree]
                deg[p.degree] = None
                # make the greater node a child
                if p.key > q.key:
                    p, q = q, p
                q.extract()
                if p.child:
                    p.child.addleft(q)
                else:
                    p.child = q
                q.parent = p
                p.degree += 1
            deg[p.degree] = p
            p = np
        # find the minroot and fix parent references
        self.minroot = None
        for root in deg:
            if root:
                root.parent = None
                if self.minroot:
                    if root.key < self.minroot.key:
                        self.minroot = root
                else:
                    self.minroot = root

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
        parent = node.parent
        if parent and node.key < parent.key:
            self.cut(node)
            self.cascading_cut(parent)
        if key < self.minroot.key:
            self.minroot = node
        return node

    def cut(self, node: HeapNode) -> None:
        """Cuts a node from its parent and adds it to the root list.

        Args:
            node (HeapNode): The node to be cut.
        """

        node.parent.child = None if node == node.left else node.left
        node.parent.degree -= 1
        node.parent = None
        node.extract()
        node.marked = False
        self.minroot.addleft(node)

    def cascading_cut(self, node: HeapNode) -> None:
        """Cuts a node and all its ancestors until an unmarked node is
            reached. Marks that node.

        Args:
            node (HeapNode): The node to start a cascading cut on.
        """

        while node.parent:
            if node.marked:
                parent = node.parent
                self.cut(node)
                node = parent
            else:
                node.marked = True
                return

    def remove(self, node: HeapNode) -> HeapNode:
        """Removes a node from the heap.

        Args:
            node (HeapNode): The node to remove.

        Returns:
            HeapNode: The removed node.
        """

        self.decreasekey(node, -math.inf)
        return self.pop()
