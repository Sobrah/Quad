import math
from node import Node
from rect import Rect
from helper import dataLength


class QuadTree:

    def __init__(self, data: list):
        self.tree_depth = 0

        # Length Of Data Image
        length = dataLength(data)

        self.tree = self.createTree(data, Rect(0, 0, length, length))

    # Create Quad Tree Recursively
    def createTree(self, data: list, rect: Rect, depth=0):
        node = Node(rect, depth)
        self.tree_depth = max(self.tree_depth, node.depth)

        # Same Elements
        if all(d == data[0] for d in data):
            node.data = data[0]

        # Divide Elements
        else:
            for i, quarterData, quarterRect in zip(
                range(4),
                self.quarterDivide(data, rect.length),
                rect.quarterDivide(),
            ):
                node.pieces[i] = self.createTree(
                    quarterData, quarterRect, node.depth + 1
                )

        return node

    # Divide Data To 4 Equal Pieces
    def quarterDivide(self, data: list, length: int):

        # Divide Into 2 Parts
        span = ((0, length // 2), (length // 2, length))

        return [
            [data[i * length + j] for i in range(*rowRange) for j in range(*colRange)]
            for rowRange in span
            for colRange in span
        ]

    # Calculate Depth Of Point Node
    def pixelDepth(self, x: int, y: int):
        depth = 0

        node = self.tree
        while node.data == None:

            # Coordinate Quadrant
            i = node.position.quadPosition(x, y)

            depth += 1
            node = node.pieces[i]

        return depth

    # Return the depth of tree
    def TreeDepth(self):
        return self.tree_depth

    # Return Image As List
    def export(self):
        length = self.tree.position.length

        # Image List
        data = [None] * length * length

        queue = [self.tree]
        while queue:
            node = queue.pop()

            # Add Subareas To Queue
            if not node.data:
                queue.extend(node.pieces)
                continue

            p = node.position
            for i in range(p.y, p.y + p.h):
                for j in range(p.x, p.x + p.w):
                    data[i * length + j] = node.data

        return data

    # Compress Image To Favorable Size
    def compress(self, size: int):
        block = self.tree.position.length // size

        queue = [self.tree]
        while queue:
            node = queue.pop()

            # Update Position
            node.position //= block

            # Leaf Reached
            if node.data:
                continue

            # Mean Of Subtrees
            if node.position.length == 1:
                node.data = self.average(node)
                node.pieces = [None] * 4

                continue

            queue.extend(node.pieces)

    # Recursively Calculate Subtree Mean
    def average(self, node: Node):

        # Leaf Reached
        if node.data:
            return node.data

        # Calculate Subtrees Mean
        averages = [self.average(piece) for piece in node.pieces]

        # Mean Of Each Channel
        return tuple(sum(c) // len(c) for c in zip(*averages))
