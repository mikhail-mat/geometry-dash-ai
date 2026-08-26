from .constants import GROUND_Y


class Obstacle:
    def __init__(self, x, y=GROUND_Y, width=100, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def left(self): return self.x

    @property
    def right(self): return self.x + self.width
    
    @property
    def top(self): return self.y - self.height

    @property
    def bottom(self): return self.y


class Block(Obstacle):
    type='block'
    def __init__(self, x, y=GROUND_Y, width=100, height=50):
        super().__init__(x, y, width, height)


class Spike(Obstacle):
    type='spike'
    def __init__(self, x, y=GROUND_Y, side_length=50):
        height = side_length * (3 ** 0.5) / 2
        super().__init__(x, y, side_length, height)

    @property
    def apex(self): return (self.x + self.width*0.5, self.top)


obstacles = [
    Spike(600),
    Block(900),
    Spike(1200),
    Spike(1250),
    Spike(1300),
    Block(1600),
    Block(1700)
]
