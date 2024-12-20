import math
from node import Node
from rect import Rect


class QuadTree:

    def __init__(self, data: list):

        # Length Of Data Image
        length = int(math.sqrt(len(data)))

        self.tree = self.createTree(data, Rect(0, 0, length, length))

    # Create Quad Tree Recursively
    def createTree(self, data: list, rect: Rect):
        node = Node(rect)

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
                node.pieces[i] = self.createTree(quarterData, quarterRect)

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
