class Rect:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __ifloordiv__(self, size: int):
        self.x //= size
        self.y //= size
        self.w //= size
        self.h //= size

        return self

    # Divide Rectangle To 4 Equal Pieces
    def quarterDivide(self):
        hw = self.w // 2
        hh = self.h // 2

        calcX = lambda x, i: x + i % 2 * hw
        calcY = lambda y, i: y + i // 2 * hh

        return [Rect(calcX(self.x, i), calcY(self.y, i), hw, hh) for i in range(4)]

    # Detect Coordinate Quadrant Of Point
    def quadPosition(self, x, y):

        # Calculate Middle
        middleX = self.x + self.w // 2
        middleY = self.y + self.h // 2

        # Detect Quarter
        i = 0 if y - middleY < 0 else 1
        j = 0 if x - middleX < 0 else 1

        return 2 * i + j
      
    @property
    def vertices(self):
        top_left = {'x': self.x, 'y': self.y}
        top_right = {'x': self.x + self.w, 'y': self.y}
        down_left = {'x': self.x, 'y': self.y + self.h}
        down_right = {'x': self.x + self.w, 'y': self.y + self.h}
    
        return [top_left, top_right, down_left, down_right]
    
    def doOverlap(self, rect):
        if self.vertices[0]['x'] >= rect.vertices[3]['x'] or self.vertices[3]['x'] <= rect.vertices[0]['x']:
            return False
        
        if self.vertices[0]['y'] >= rect.vertices[3]['y'] or self.vertices[3]['y'] <= rect.vertices[0]['y']:
            return False
        
        return True
             
    @property
    def length(self):
        if self.w == self.h:
            return self.w

        return None
