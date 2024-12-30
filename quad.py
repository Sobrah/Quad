from rect import Rect
from node import Node
import numpy as np


class QuadTree:

    def __init__(self, data: np.ndarray):
        self.tree = self.createTree(data, Rect(0, 0, len(data[0]), len(data)))

    # Create Quad Tree Recursively
    def createTree(self, data: np.ndarray, rect: Rect):
        node = Node(rect)

        # Same Elements
        if (data[i, j] == data[0, 0] for i in range(len(data)) for j in range(len(data[0]))):
            node.data = data[0, 0]

        # Divide Elements
        else:
            for quarterData, quarterRect in zip(
                self.quarterDivide(data, rect.length), rect.quarterDivide()
            ):
                node.pieces.append(self.createTree(quarterData, quarterRect))

        return node

    # Divide Data To 4 Equal Pieces
    def quarterDivide(self, data: np.ndarray, length: int):

        # Divide Into 2 Parts
        span = ((0, length // 2), (length // 2, length))

        return [
            # [data[length * i + j] for i in range(*rowRange) for j in range(*colRange)]
            [data[i, j] for i in range(*rowRange) for j in range(*colRange)]
            for rowRange in span
            for colRange in span
        ]

    # Calculate Depth Of Point Node
    def pixelDepth(self, x: int, y: int):
        depth = 0

        node = self.tree
        while not node.data:

            # Coordinate Quadrant
            i = node.position.quadPosition(x, y)

            depth += 1
            node = node.pieces[i]

        return depth

    # Return the depth of tree
    def treeDepth(self):
        def traverse(node: Node, depth: int):

            # Leaf Reached
            if node.data:
                return depth

            return max([traverse(piece, depth + 1) for piece in node.pieces])

        return traverse(self.tree, 0)

    # Return Image As List
    def export(self):
        length = self.tree.position.length

        # Image List
        data = np.array((length, length))
        data[:] = None
        # data = [None] * length * length

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
                    data[i, j] = node.data
                    # data[i * length + j] = node.data

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
        if node.data:
            return node.data

        # Calculate Subtrees Mean
        averages = [self.average(piece) for piece in node.pieces]

        # Mean Of Each Channel
        return tuple(sum(c) // len(c) for c in zip(*averages))

    # Return Subspaces Within Rectangle
    def searchSubspaces(self, rect: Rect, reverse: bool = False):

        # Leaves Within Rect
        leaves = self.collisionNodes(self.tree, rect)

        # Create Base Rectangle
        base = Rect(
            bx := min(leaf.position.x for leaf in leaves),
            by := min(leaf.position.y for leaf in leaves),
            max(leaf.position.ex for leaf in leaves) - bx,
            max(leaf.position.ey for leaf in leaves) - by,
        )

        # Create base subimage
        if not reverse:
            
            # Create Empty Image
            data = np.ndarray((base.w, base.h), dtype=object)
            data[:] = (0, 0, 0, 0)
            # data = [(0, 0, 0, 0)] * base.w * base.h
        else:
            
            # Create Full Image
            image = self.export()
            data = [
                    image[y, x]
                    # image[y * base.w + x]
                    for y in range(base.y, base.h)
                    for x in range(base.x, base.w)
                    ]
            

        # Initialize leave's pixel's color within the subimage 
        for leaf in leaves:
            for i in range(leaf.position.y - base.y, leaf.position.ey - base.y):
                for j in range(leaf.position.x - base.x, leaf.position.ex - base.x):
                    data[i, j] = leaf.data if not reverse else (0, 0, 0, 0)
                    # data[i * base.w + j] = leaf.data if not reverse else (0, 0, 0, 0)

        return data, (base.w, base.h)

    # Remove Subspaces Withing Rectangle From Original Image
    def mask(self, rect: Rect):
        return self.searchSubspaces(rect, True)

    # Returns Leaves Inside Rectangle
    def collisionNodes(self, root: Node, rect: Rect):
        results = []

        stack = [root]
        while stack:
            node = stack.pop()

            if node.data:
                results.append(node)

            for piece in node.pieces:
                if piece.position.overlap(rect):
                    stack.append(piece)

        return results

    # Compress A Sequence Of Image Data
    @classmethod
    def sequenceCompress(cls, data: list, size: int):
        results = []
        for frame in data:
            q = cls(frame)
            q.compress(size)

            results.append(q.export())
        return results
