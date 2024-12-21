from rect import Rect


class Node:
    def __init__(self, position: Rect, depth: int):
        self.data = None
        self.position = position
        self.pieces = [None, None, None, None]
        self.depth = depth
