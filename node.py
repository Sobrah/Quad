from rect import Rect


class Node:
    def __init__(self, position: Rect):
        self.data = None
        self.position = position
        self.pieces = []
