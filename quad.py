import math
from node import Node
from rect import Rect
from helper import dataLength
from helper import listToImage


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
            [data[length * i + j] for i in range(*rowRange) for j in range(*colRange)]
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
        if node.data:
            return node.data

        # Calculate Subtrees Mean
        averages = [self.average(piece) for piece in node.pieces]

        # Mean Of Each Channel
        return tuple(sum(c) // len(c) for c in zip(*averages))

    def searchSubspacesWithRange(
        self, x1: int, y1: int, x2: int, y2: int, reverse: bool = False
    ):

        # Get leaves as a list
        leaves = self.getNodesInRectangle(
            root=self.tree, rect=Rect(x1, y1, x2 - x1, y2 - y1)
        )

        top, right, down, left = y1, x2, y2, x1

        # Find the edges of final rectangle
        for leaf in leaves:
            top = min(top, leaf.position.y)
            right = max(right, leaf.position.x + leaf.position.w)
            down = max(down, leaf.position.y + leaf.position.h)
            left = min(left, leaf.position.x)

        # Generate an empty image
        rectPixels = [
            {
                "x": x,
                "y": y,
                "data": (
                    (0, 0, 0, 0) if not reverse else self.getPixelData(self.tree, x, y)
                ),
            }
            for y in range(top, down)
            for x in range(left, right)
        ]

        # Add pixel nodes to rectangle
        for p in rectPixels:
            for leaf in leaves:
                lp = leaf.position
                if (
                    lp.vertices[0]["x"] <= p["x"] < lp.vertices[3]["x"]
                    and lp.vertices[0]["y"] <= p["y"] < lp.vertices[3]["y"]
                ):
                    p["data"] = leaf.data if not reverse else (0, 0, 0, 0)
                    break

        listToImage(
            "searchSubspacesWithRange.png" if not reverse else "mask.png",
            [pixel["data"] for pixel in rectPixels],
            right - left,
            down - top,
        )

    # Remover all nodes that are partially or completely inside the given range.
    def mask(self, x1: int, y1: int, x2: int, y2: int):
        self.searchSubspacesWithRange(x1, y1, x2, y2, reverse=True)

    # Returns all leaves inside the given rectangle
    def getNodesInRectangle(self, root: Node, rect: Rect, output: list = []):

        # Go deeper if node is not leaf
        if root.data == None:
            for piece in root.pieces:
                output = self.getNodesInRectangle(root=piece, rect=rect)

        elif root.position.doOverlap(rect):
            output.append(root)

        return output

    def getPixelData(self, root: Node, x: int, y: int):
        if root.data == None:
            for piece in root.pieces:
                data = self.getPixelData(piece, x, y)
                if data != None:
                    return data

        v = root.position.vertices
        if v[0]["x"] <= x < v[3]["x"] and v[0]["y"] <= y < v[3]["y"]:
            return root.data

    # Compress A Sequence Of Image Data
    @classmethod
    def sequenceCompress(cls, data: list, size: int):
        results = []
        for frame in data:
            q = cls(frame)
            q.compress(size)

            results.append(q.export())
        return results
