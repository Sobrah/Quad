class Rect:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    # Divide Rectangle To 4 Equal Pieces
    def quarterDivide(self):
        hw = self.w // 2
        hh = self.h // 2

        calcX = lambda x, i: x + i % 2 * hw
        calcY = lambda y, i: y + i // 2 * hh

        return [Rect(calcX(self.x, i), calcY(self.y, i), hw, hh) for i in range(4)]

    @property
    def length(self):
        if self.w == self.h:
            return self.w

        return None
