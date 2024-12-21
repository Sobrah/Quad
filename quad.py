import math
from node import Node
from rect import Rect


class QuadTree:

    def __init__(self, data: list):
        self.tree_depth = 0

        # Length Of Data Image
        length = int(math.sqrt(len(data)))

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
                node.pieces[i] = self.createTree(quarterData, quarterRect, node.depth + 1)

        return node

    # Divide Data To 4 Equal Pieces
    def quarterDivide(self, data: list, length: int):

        # Divide Into 2 Parts
        span = ((0, length // 2), (length // 2, length))

        result = []
        for rowRange in span:
            for colRange in span:
                result.append(
                    [
                        data[length * i + j]
                        for j in range(*colRange)
                        for i in range(*rowRange)
                    ]
                )

        return result

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
