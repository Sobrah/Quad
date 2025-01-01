from rect import Rect
from node import Node
from math import log2 as log


class QuadTree:

    def __init__(self, data: list):
        self.tree = self.createTree(data, Rect(0, 0, len(data), len(data)))

    # Create Quad Tree Recursively
    def createTree(self, data: list, rect: Rect):
        node = Node(rect)

        # Same Elements
        if all(all(data[0][0] == col for col in row) for row in data):
            node.data = data[0][0]

        # Divide Elements
        else:
            for quarterData, quarterRect in zip(
                self.quarterDivide(data, rect.length), rect.quarterDivide()
            ):
                node.pieces.append(self.createTree(quarterData, quarterRect))

        return node

    # Divide Data To 4 Equal Pieces
    def quarterDivide(self, data, length: int):

        # Divide Into 2 Parts
        span = ((0, length // 2), (length // 2, length))

        return [
            [[data[i][j] for j in range(*colRange)] for i in range(*rowRange)]
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
        data = [[None] * length for i in range(length)]

        stack = [self.tree]
        while stack:
            node = stack.pop()

            # Add Subareas To Queue
            if not node.data:
                stack.extend(node.pieces)
                continue

            p = node.position
            for i in range(p.y, p.ey):
                for j in range(p.x, p.ex):
                    data[i][j] = node.data

        return data

    # Compress Image To Favorable Size
    def compress(self, size: int):
        block = self.tree.position.length // size

        stack = [self.tree]
        while stack:
            node = stack.pop()

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

            stack.extend(node.pieces)

    # Recursively Calculate Subtree Mean
    def average(self, node: Node):
        if node.data:
            return node.data

        # Calculate Subtrees Mean
        averages = [self.average(piece) for piece in node.pieces]

        # Mean Of Each Channel
        return tuple(sum(c) // len(c) for c in zip(*averages))

    # Search Subspaces Within Rectangle
    def search(self, rect: Rect, reverse: bool):

        # Leaves Within Rect
        leaves = self.collisionNodes(self.tree, rect, reverse)

        # Create Base Rectangle
        base = Rect(
            bx := min(leaf.position.x for leaf in leaves),
            by := min(leaf.position.y for leaf in leaves),
            max(leaf.position.ex for leaf in leaves) - bx,
            max(leaf.position.ey for leaf in leaves) - by,
        )
        
        if not reverse:
            max_dim = max(base.h, base.w)
            while not log(max_dim).is_integer(): max_dim += 1
            base.w = base.h = max_dim
        
        # Create Empty Image
        data = [[(0, 0, 0, 0)] * base.w for i in range(base.h)]

        for leaf in leaves:
            for i in range(leaf.position.y - base.y, leaf.position.ey - base.y):
                for j in range(leaf.position.x - base.x, leaf.position.ex - base.x):
                    data[i][j] = leaf.data

        # return data
        return QuadTree(data)

    # Return Subspaces Within Rectangle
    def searchSubspaces(self, rect: Rect):
        return self.search(rect, False)

    # Remove Subspaces Withing Rectangle From Original Image
    def mask(self, rect: Rect):
        return self.search(rect, True)

    # Returns Leaves Inside Rectangle
    def collisionNodes(self, root: Node, rect: Rect, reverse: bool):
        results = []

        stack = [root]
        while stack:
            node = stack.pop()

            # Leaf Reached
            if node.data:
                if node.position.overlap(rect) ^ reverse:
                    results.append(node)

            stack.extend(node.pieces)

        return results

    # Compress Image
    @classmethod
    def compressData(cls, data: list, size: int):
        q = cls(data)
        q.compress(size)

        return q.export()
    

