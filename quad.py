import math
from node import Node


class QuadTree:
    def __init__(self, data: list):
        self.tree = self.createTree(data)

    # Create Quad Tree Recursively
    def createTree(self, data: list):
        node = Node()

        # Same Elements
        if all(d == data[0] for d in data):
            node.data = data[0]

        # Divide Elements
        else:
            for i, quarter in enumerate(self.quarterDivide(data)):
                node.pieces[i] = self.createTree(quarter)

        return node

    # Divide Data To 4 Equal Pieces
    def quarterDivide(self, data: list):

        # Length Of Data
        length = int(math.sqrt(len(data)))

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
